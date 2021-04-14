import ctypes.wintypes
from aiohttp import web
import time
import os
from FFxivPythonTrigger import PluginBase, api
import win32con

_pid = os.getpid()
_p_hwnds = []


def _filter_func(hwnd, param):
    rtn_value = ctypes.wintypes.DWORD()
    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(rtn_value))
    if rtn_value.value == _pid:
        str_buffer = (ctypes.c_char * 512)()
        ctypes.windll.user32.GetClassNameA(hwnd, str_buffer, 512)
        if str_buffer.value == b'FFXIVGAME':
            _p_hwnds.append(hwnd)


_c_filter_func = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)(_filter_func)
ctypes.windll.user32.EnumWindows(_c_filter_func, 0)


class KeyApi:
    @staticmethod
    def key_down(key_code: int):
        for hwnd in _p_hwnds:
            ctypes.windll.user32.SendMessageA(hwnd, win32con.WM_KEYDOWN, key_code, 0)

    @staticmethod
    def key_up(key_code: int):
        for hwnd in _p_hwnds:
            ctypes.windll.user32.SendMessageA(hwnd, win32con.WM_KEYUP, key_code, 0)

    @staticmethod
    def key_press(key_code: int, time_ms: int = 10):
        KeyApi.key_down(key_code)
        time.sleep(time_ms / 1000)
        KeyApi.key_up(key_code)


class SendKeys(PluginBase):
    name = "SendKeys"

    async def text_command_handler(self, request: web.Request):
        try:
            code = int(await request.text())
            KeyApi.key_press(code)
        except TypeError:
            return web.json_response({
                'msg': 'failed',
                'rtn': 'type error'
            })
        else:
            return web.json_response({
                'msg': 'success',
                'rtn': code
            })

    def __init__(self):
        super().__init__()
        self.api_class = KeyApi()
        self.register_api("SendKeys", self.api_class)
        api.HttpApi.register_post_route('sendkey', self.text_command_handler)
