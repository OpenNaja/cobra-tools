from generated.array import Array
from generated.formats.fct.structs.Font import Font
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class FctRoot(MemStruct):
    u_0: int
    u_1: int
    a: float
    b: float
    c: float
    minus_1: int
    z_0: int
    z_1: int
    z_2: int
    offset: int
    fonts: Array[Font]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
