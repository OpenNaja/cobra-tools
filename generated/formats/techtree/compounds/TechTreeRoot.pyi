from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.techtree.compounds.TechLevel import TechLevel


class TechTreeRoot(MemStruct):
    filename: Pointer[str]
    buffer_0: int
    buffer_1: int
    tech_levels: ArrayPointer[TechLevel]
    tech_levels_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
