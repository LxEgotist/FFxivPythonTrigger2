from sys import platform, version_info
from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy

if platform == "win32" and version_info >= (3, 8, 0):
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())

from FFxivPythonTrigger import *

Logger.print_log_level = Logger.DEBUG
try:
    register_module("SocketLogger")
    register_modules(["HttpApi", "XivMemory", "XivMagic", "Command", "LogHookFix"])
    register_modules(["CutsceneSkipper", "SuperJump", "Zoom", "Teleporter","XivCombo"])
    register_modules(["DebugExec"])
    start()
except Exception:
    pass
finally:
    close()
