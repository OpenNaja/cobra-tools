from generated.array import Array
from generated.formats.landscape.structs.BufferPresence import BufferPresence
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class LandscapeRoot(MemStruct):
    pointers_1: Array[int]
    buffer_pointers: ArrayPointer[BufferPresence]
    pointers_2: Array[int]
    size: int
    a: int
    b: int
    rest: Array[int]
    name_buffer_size: int
    rest_2: Array[int]
    things_count: int
    rest_3: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
