from generated.formats.achievements.compounds.ConditionRef2 import ConditionRef2
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ConditionRef2Ptr(MemStruct):
    ptr: Pointer[ConditionRef2]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
