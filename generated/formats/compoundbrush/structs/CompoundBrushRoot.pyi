from generated.formats.compoundbrush.structs.BrushStruct import BrushStruct
from generated.formats.compoundbrush.structs.SomeStruct3 import SomeStruct3
from generated.formats.compoundbrush.structs.SomeStruct4 import SomeStruct4
from generated.formats.compoundbrush.structs.SomeStruct4Sub2 import SomeStruct4Sub2
from generated.formats.compoundbrush.structs.SomeStruct8 import SomeStruct8
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.ovl_base.compounds.ZStringList import ZStringList


class CompoundBrushRoot(MemStruct):
    brushes: ArrayPointer[BrushStruct]
    pointer_2: Pointer[ZStringList]
    pointer_3: ArrayPointer[SomeStruct3]
    pointer_4: ArrayPointer[SomeStruct4]
    pointer_5: Pointer[ZStringList]
    pointer_6: Pointer[ZStringList]
    pointer_7: ArrayPointer[SomeStruct4Sub2]
    pointer_8: Pointer[SomeStruct8]
    mask_name: Pointer[str]
    brushes_count: int
    unknown_2_count: int
    unknown_3_count: int
    unknown_4_count: int
    unknown_5_count: int
    unknown_6_count: int
    unknown_7_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
