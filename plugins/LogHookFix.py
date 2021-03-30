import ctypes
from FFxivPythonTrigger import PluginBase, api
from FFxivPythonTrigger.hook import Hook
from FFxivPythonTrigger.memory import scan_pattern
from FFxivPythonTrigger.Logger import Logger
from FFxivPythonTrigger.Storage import get_module_storage
from FFxivPythonTrigger.AddressManager import AddressManager
from traceback import format_exc

_logger = Logger("LogHookFix")
_storage = get_module_storage("LogHookFix")
_am = AddressManager(_storage.data, _logger)
sig = "48 89 ? ? ? 48 89 ? ? ? 48 89 ? ? ? 57 41 ? 41 ? 48 83 EC ? 48 8B ? ? 48 8B ? 48 2B ? ? 4C 8B"
addr = _am.get("addr", scan_pattern, sig)
_storage.save()


class LogHook(Hook):
    restype = ctypes.c_uint
    argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_int]

    def hook_function(self, a1, a2, a3):
        try:
            new_addr = a1 - 72
            if api.XivMemory.chat_log is None or ctypes.addressof(api.XivMemory.chat_log) != new_addr:
                _logger.info("fix chat log base address to %s" % hex(new_addr))
                api.XivMemory.set_chat_log_table(new_addr)
            else:
                _logger.debug("chat log base address is correct")
            self.uninstall()
        except Exception:
            _logger.error(format_exc())
        return self.original(a1, a2, a3)


class LogHookFix(PluginBase):
    name = "log hook fix"

    def __init__(self):
        super(LogHookFix, self).__init__()
        self.hook = LogHook(addr)
        self.hook.enable()

    def _onunload(self):
        self.hook.uninstall()
