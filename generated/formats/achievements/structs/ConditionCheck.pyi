from generated.formats.achievements.structs.ConditionPc2 import ConditionPc2
from generated.formats.achievements.structs.ConditionRef2Ptr import ConditionRef2Ptr
from generated.formats.achievements.structs.ConditionRefPtr import ConditionRefPtr
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class ConditionCheck(MemStruct):
    condition_name: Pointer[str]
    condition_index: int
    condition_index_str: Pointer[str]
    count: int
    zero: Pointer[ConditionPc2]
    conditions_2: ArrayPointer[ConditionRef2Ptr]
    conditions_2_count: int
    conditions: ArrayPointer[ConditionRefPtr]
    conditions_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
