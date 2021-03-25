from FFxivPythonTrigger.memory import scan_address, scan_pattern
from FFxivPythonTrigger.Logger import Logger
from FFxivPythonTrigger.Storage import get_module_storage
from FFxivPythonTrigger.AddressManager import AddressManager

_logger = Logger("XivMagic/AddressManager")
_storage = get_module_storage("XivMagic")
_am = AddressManager(_storage.data, _logger)

##########
# do text command
##########
do_text_command_sig = "48 89 5C 24 ?? 57 48 83 EC 20 48 8B FA 48 8B D9 45 84 C9"
do_text_command_addr = _am.get("text command function", scan_pattern, do_text_command_sig)
text_command_ui_module_ptr_sig = "48 8B 05 ?? ?? ?? ?? 48 8B D9 8B 40 14 85 C0"
text_command_ui_module_ptr_addr = _am.get("text command ui module pointer", scan_address, text_command_ui_module_ptr_sig, cmd_len=7)

_storage.save()
