from traceback import format_exc
from typing import List, Tuple

from FFxivPythonTrigger.Logger import Logger
from FFxivPythonTrigger.hook import Hook
from ctypes import *

_logger = Logger("frame inject")

_continue_works = dict()
_once_works: List[Tuple[callable, list, dict]] = list()


class FrameInjectHook(Hook):
    _continue_works = dict()
    _once_works: List[Tuple[callable, list, dict]] = list()

    def register_continue_call(self, call, *args, **kwargs):
        _continue_works[call] = (args, kwargs)

    def unregister_continue_call(self, call):
        del _continue_works[call]

    def register_once_call(self, call, *args, **kwargs):
        _once_works.append((call, args, kwargs))

    argtypes = [c_void_p, c_void_p]

    def hook_function(self, *oargs):
        try:
            while _once_works:
                try:
                    c, a, k = _once_works.pop(0)
                    c(*a, **k)
                except Exception:
                    _logger.error("error in frame call:\n" + format_exc())
            for c, v in _continue_works.copy().items():
                try:
                    c(*v[0], **v[1])
                except Exception:
                    del _continue_works[c]
                    _logger.error("error in frame call, continue work will be removed:\n" + format_exc())
        except Exception:
            _logger.error("error in frame inject:\n" + format_exc())
        return self.original(*oargs)


def register_continue_call(call, *args, **kwargs):
    _continue_works[call] = (args, kwargs)


def unregister_continue_call(call):
    del _continue_works[call]


def register_once_call(call, *args, **kwargs):
    _once_works.append((call, args, kwargs))
