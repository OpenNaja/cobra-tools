from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.physicssurfacesxmlres.compounds.Struct2Sub import Struct2Sub


class Struct2(MemStruct):
    name_1: Pointer[str]
    arr: ArrayPointer[Struct2Sub]
    count: int
    short_2: int
    unk_32_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
