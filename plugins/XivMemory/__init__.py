from FFxivPythonTrigger import PluginBase, Logger, memory
from . import ActorTable, CombatData, PlayerInfo, Targets, AddressManager

_logger = Logger.Logger("XivMem")


class XivMemory(object):
    actor_table = ActorTable.actor_table
    combat_data = CombatData.combat_data
    player_info = PlayerInfo.player_info
    targets = Targets.targets

    @property
    def zone_id(self):
        return memory.read_uint(AddressManager.zone_addr)


class XivMemoryPlugin(PluginBase):
    name = "XivMemory"

    def __init__(self):
        super(XivMemoryPlugin, self).__init__()
        self.apiClass = XivMemory()
        self.register_api('XivMemory', self.apiClass)
        self.work = False

    def _onunload(self):
        self.work = False
