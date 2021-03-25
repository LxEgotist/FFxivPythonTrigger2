from FFxivPythonTrigger.memory import scan_address, write_float,read_float
from FFxivPythonTrigger.Logger import Logger
from FFxivPythonTrigger.Storage import get_module_storage
from FFxivPythonTrigger.AddressManager import AddressManager
from FFxivPythonTrigger import FFxiv_Version, PluginBase, api

"""
change the jump value to let you jump higher -- or lower
command:    @sjump
format:     /e @sjump [func] [args]...
functions (*[arg] is optional args):
    [get]:      get current jump value
    [set]:      set current jump value
                format: /e @sjump set [value(float) / "default"]
"""

command = "@sjump"

_logger = Logger("SuperJump")
_storage = get_module_storage("SuperJump")
sig = "f3 0f 10 35 ?? ?? ?? ?? 48 85 c0 74 ?? 48 8b 88 ?? ?? ?? ?? 48 85 c9 75 ?? 32 c0 eb ?? f6 05 ?? ?? ?? ?? ?? 75 ?? 33 d2 e8 ?? ?? ?? ?? f6 d8 " \
    "0f 28 d6 48 8b cb 1b d2 83 c2 ?? 0f 28 74 24 ?? 48 83 c4 ?? 5b e9 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? 40 53 "
addr = AddressManager(_storage.data, _logger).get("addr", scan_address, sig,cmd_len=8)
_storage.save()

default = 10.4

class CutsceneSkipper(PluginBase):
    name = "Cutscene Skipper"

    def __init__(self):
        super().__init__()
        api.command.register(command, self.process_command)

    def _onunload(self):
        api.command.unregister(command)

    def process_command(self, args):
        api.Magic.echo_msg(self._process_command(args))

    def _process_command(self, arg):
        try:
            if arg[0] == "set":
                if arg[1] == 'default':
                    arg[1] = default
                write_float(addr, float(arg[1]))
                return "set to %s" % arg[1]
            elif arg[0] == "get":
                return read_float(addr)
            else:
                return "unknown arg [%s]" % arg[0]
        except Exception as e:
            return str(e)
