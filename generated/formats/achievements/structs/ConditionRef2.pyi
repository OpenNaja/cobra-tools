from generated.formats.achievements.structs.ConditionRef import ConditionRef
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class ConditionRef2(MemStruct):
    ref_name: Pointer[str]
    mode: int
    condition_ref: Pointer[ConditionRef]
    count: int
    zero_1: int
    zero_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
