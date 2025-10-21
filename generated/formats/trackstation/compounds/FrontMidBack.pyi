from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class FrontMidBack(MemStruct):
    front: Pointer[str]
    middle: Pointer[str]
    back: Pointer[str]
    front_rotation: int
    middle_rotation: int
    back_rotation: int
    unkown_byte_0: int
    unkown_byte_1: int
    unkown_byte_2: int
    unkown_byte_3: int
    unkown_byte_4: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
