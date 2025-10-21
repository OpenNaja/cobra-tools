from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class SomeStruct4Sub2(MemStruct):
    some_struct_4_sub_2_string: Pointer[str]
    unknown_1_int: int
    unknown_1_float: float
    unknown_2_float: float
    unknown_3_float: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
