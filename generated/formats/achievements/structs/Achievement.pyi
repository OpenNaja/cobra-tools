from generated.array import Array
from generated.formats.achievements.structs.ConditionRefPtr import ConditionRefPtr
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class Achievement(MemStruct):
    achievement_name: Pointer[str]
    conditions: ArrayPointer[ConditionRefPtr]
    conditions_count: int
    minus_one_1: int
    minus_one_2: int
    zero_1: int
    zero_2: int
    flags: Array[int]
    zero_3: int
    zero_4: int
    zero_5: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
