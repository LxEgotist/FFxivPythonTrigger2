from traceback import format_exc

from .struct.ChatLog import ChatLogTable as ChatLogTableStruct
from .chatLog import ChatLog, Player
from FFxivPythonTrigger import EventBase, Logger, memory
from datetime import datetime
from . import AddressManager

has_fix_patch=True

_logger = Logger.Logger("XivMem/ChatLog")


class ChatLogTable(ChatLogTableStruct):
    def get(self, idx: int):
        return ChatLog(self.get_raw(idx))


_sig = hex(AddressManager.chat_log_addr)[2:].zfill(16)
_sig = " ".join([_sig[i * 2:i * 2 + 2] for i in range(7, -1, -1)])

chat_log_addr = memory.pattern.brute_scan(memory.ida_sig_to_pattern(_sig)) if not has_fix_patch else None
if chat_log_addr is not None:
    _logger.debug("chat log table found at %s" % hex(chat_log_addr))
    chat_log: ChatLogTable = memory.read_memory(ChatLogTable, chat_log_addr)
else:
    _logger.warning("chat log table not found")
    chat_log = None


class ChatLogEvent(EventBase):
    id = "log_event"
    name = "log event"

    def __init__(self, chat_log: ChatLog):
        self.time = datetime.fromtimestamp(chat_log.time)
        self.channel_id = chat_log.channel_id
        self.player = self.player_server = None
        for msg in chat_log.grouped_sender:
            if isinstance(msg, Player):
                self.player = msg.playerName
                self.player_server = msg.serverId
        self.message = chat_log.text
        self.chat_log = chat_log

    def __str__(self):
        return "{}\t{}\t{}\t{}".format(self.time, self.channel_id, self.player or 'n/a', self.message)

    def get_dict(self):
        return {
            't': self.chat_log.time,
            'c': self.channel_id,
            's': self.player,
            'ss': self.player_server,
            'm': self.message
        }


class ChatLogProcessor(object):
    def __init__(self):
        self.update_sign = None
        self.msg_count = None

    def check_update(self):
        ans = []
        if chat_log is not None:
            new_sign = chat_log.check_update
            if self.update_sign != new_sign:
                self.update_sign = new_sign
                self.msg_count = chat_log.count
            new_count = chat_log.count
            while self.msg_count < new_count:
                try:
                    ans.append(ChatLogEvent(chat_log.get(self.msg_count)))
                except:
                    _logger.error('error on parsing chat log:\n'+format_exc())
                self.msg_count += 1
        return ans


processor = ChatLogProcessor()
