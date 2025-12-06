from generated.formats.base.structs.Vector3 import Vector3
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class Row(MemStruct):
    offset: float
    offset_align: int
    seats: ArrayPointer[Vector3]
    seats_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
