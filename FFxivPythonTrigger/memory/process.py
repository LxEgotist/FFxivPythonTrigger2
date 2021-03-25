from ctypes import *
from ctypes import wintypes
from .res import kernel32, psapi, structure
from . import exception

CURRENT_PROCESS_HANDLER = kernel32.GetCurrentProcess()


def virtual_query(address):
    mbi = structure.MEMORY_BASIC_INFORMATION()
    kernel32.VirtualQueryEx(CURRENT_PROCESS_HANDLER, address, byref(mbi), sizeof(mbi))
    return mbi


def get_current_process_filename(length: int = wintypes.MAX_PATH, coding: str = structure.DEFAULT_CODING):
    buff = create_string_buffer(length)
    windll.kernel32.SetLastError(0)
    rl = kernel32.GetModuleFileName(None, byref(buff), length)
    error_code = windll.kernel32.GetLastError()
    if error_code:
        windll.kernel32.SetLastError(0)
        raise exception.WinAPIError(error_code)
    raw = buff.raw
    return raw[:rl].decode(coding)


def base_module():
    hModules = (c_void_p * 1024)()
    process_module_success = psapi.EnumProcessModulesEx(
        CURRENT_PROCESS_HANDLER,
        byref(hModules),
        sizeof(hModules),
        byref(c_ulong()),
        structure.EnumProcessModuleEX.LIST_MODULES_64BIT
    )
    error_code = windll.kernel32.GetLastError()
    if error_code:
        windll.kernel32.SetLastError(0)
        raise exception.WinAPIError(error_code)
    if not process_module_success:
        return  # xxx
    module_info = structure.MODULEINFO(CURRENT_PROCESS_HANDLER)
    psapi.GetModuleInformation(
        CURRENT_PROCESS_HANDLER,
        c_void_p(hModules[0]),
        byref(module_info),
        sizeof(module_info)
    )
    return module_info


def enum_process_module():
    hModules = (c_void_p * 1024)()
    process_module_success = psapi.EnumProcessModulesEx(
        CURRENT_PROCESS_HANDLER,
        byref(hModules),
        sizeof(hModules),
        byref(c_ulong()),
        structure.EnumProcessModuleEX.LIST_MODULES_64BIT
    )
    error_code = windll.kernel32.GetLastError()
    if error_code:
        windll.kernel32.SetLastError(0)
        raise exception.WinAPIError(error_code)
    if process_module_success:
        hModules = iter(m for m in hModules if m)
        for hModule in hModules:
            module_info = structure.MODULEINFO(CURRENT_PROCESS_HANDLER)
            psapi.GetModuleInformation(
                CURRENT_PROCESS_HANDLER,
                c_void_p(hModule),
                byref(module_info),
                sizeof(module_info)
            )
            yield module_info


def module_from_name(module_name: str):
    module_name = module_name.lower()
    modules = enum_process_module()
    for module in modules:
        if module.name.lower() == module_name:
            return module
