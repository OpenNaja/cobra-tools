from generated.formats.achievements.structs.ConditionRef import ConditionRef
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class ConditionRefPtr(MemStruct):
    ptr: Pointer[ConditionRef]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
