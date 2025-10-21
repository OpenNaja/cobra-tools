from generated.formats.compoundbrush.structs.SomeStruct4Sub2 import SomeStruct4Sub2
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class SomeStruct4Sub1(MemStruct):
    some_struct_4_sub_1_string: Pointer[str]
    some_struct_4_sub_2: ArrayPointer[SomeStruct4Sub2]
    some_struct_4_sub_2_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
