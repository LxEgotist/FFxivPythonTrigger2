from FFxivPythonTrigger import PluginBase, Logger, memory, process_event
from . import ActorTable, CombatData, PlayerInfo, Targets, AddressManager, ChatLog
from time import sleep

_logger = Logger.Logger("XivMem")


class XivMemory(object):
    actor_table = ActorTable.actor_table
    combat_data = CombatData.combat_data
    player_info = PlayerInfo.player_info
    targets = Targets.targets

    @property
    def chat_log(self):
        return ChatLog.chat_log

    def set_chat_log_table(self, address: int):
        ChatLog.chat_log = memory.read_memory(ChatLog.ChatLogTable, address)

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

    def _start(self):
        self.work = True
        while self.work:
            events = []
            events += ChatLog.processor.check_update()
            for event in events:
                process_event(event)
            sleep(0.1)
