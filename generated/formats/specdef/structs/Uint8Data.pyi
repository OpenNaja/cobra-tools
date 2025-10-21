from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class Uint8Data(MemStruct):
    imin: int
    imax: int
    ivalue: int
    ioptional: int
    unused: Array[int]
    enum: Pointer[object]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
