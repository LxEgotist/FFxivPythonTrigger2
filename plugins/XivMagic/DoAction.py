from FFxivPythonTrigger.memory import *

do_action_func_addr = BASE_ADDR + 0x7FA530
action_sub_addr = BASE_ADDR + 0x1CB90D0

_do_action_func = CFUNCTYPE(c_int64, c_int64, c_uint, c_uint, c_int64, c_uint, c_uint, c_int)(do_action_func_addr)


def do_action(action_type, action_id, target_id=0xE0000000, unk1=0, unk2=0, unk3=0):
    return _do_action_func(action_sub_addr, action_type, action_id, target_id, unk1, unk2, unk3)


def use_skill(skill_id, target_id=0xE0000000):
    return do_action(1, skill_id, target_id)


def use_item(item_id, target_id=0xE0000000, block_id=65535):
    return do_action(2, item_id, target_id, block_id)


def ride_mount(mount_id):
    return do_action(13, mount_id)


def call_minion(minion_id):
    return do_action(8, minion_id)


def fashion_item(item_id):
    return do_action(20, item_id)


def common_skill_id(skill_id, target_id=0xE0000000):
    return do_action(5, skill_id, target_id)
