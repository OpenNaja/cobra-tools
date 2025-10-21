from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class Data(MemStruct):
    floats: Array[float]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
