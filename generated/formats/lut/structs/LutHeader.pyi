from generated.formats.base.structs.Vector3 import Vector3
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class LutHeader(MemStruct):
    _colors: ArrayPointer[Vector3]
    colors_count: int
    unk_0: int
    unk_1: int
    colors_in_column_count: int
    dimensions: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
