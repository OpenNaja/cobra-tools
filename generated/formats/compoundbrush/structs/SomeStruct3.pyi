from generated.array import Array
from generated.formats.compoundbrush.structs.SomeStruct3Sub1 import SomeStruct3Sub1
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class SomeStruct3(MemStruct):
    brush_name: Pointer[str]
    unknown_struct_1: ArrayPointer[SomeStruct3Sub1]
    unknown_struct_2: ArrayPointer[SomeStruct3Sub1]
    unknown_int_1: int
    some_struct_3_sub_1_count: int
    unknown_ints: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
