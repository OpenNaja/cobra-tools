from generated.formats.compoundbrush.structs.SomeStruct4Sub1 import SomeStruct4Sub1
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class SomeStruct4(MemStruct):
    brush_name: Pointer[str]
    some_struct_4_sub_1: Pointer[SomeStruct4Sub1]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
