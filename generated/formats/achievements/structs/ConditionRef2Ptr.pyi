from generated.formats.achievements.structs.ConditionRef2 import ConditionRef2
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class ConditionRef2Ptr(MemStruct):
    ptr: Pointer[ConditionRef2]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
