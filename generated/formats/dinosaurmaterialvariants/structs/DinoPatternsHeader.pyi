from generated.formats.dinosaurmaterialvariants.structs.CommonHeader import CommonHeader
from generated.formats.dinosaurmaterialvariants.structs.Pattern import Pattern
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.Pointer import Pointer


class DinoPatternsHeader(CommonHeader):
    set_count: int
    set_name: Pointer[str]
    patterns: ArrayPointer[Pattern]
    pattern_count: int
    zero: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
