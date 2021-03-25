from FFxivPythonTrigger.memory.StructFactory import OffsetStruct
from ctypes import *


class ChatLogTable(OffsetStruct({
    'count': (c_ulong, 5 * 4),
    'check_update': (c_ulonglong, 5 * 8),
    'lengths': (POINTER(c_uint), 9 * 8),
    'data': (POINTER(c_ubyte), (12 * 8))
})):
    def get_raw(self, idx: int):
        if idx < 0:
            idx = self.count + idx
        if not max(-1, self.count - 1000) < idx < self.count:
            raise IndexError('list index %s out of range' % idx)
        idx %= 1000
        start = self.lengths[idx - 1] if idx > 0 else 0
        return bytes(self.data[start:self.lengths[idx]])
