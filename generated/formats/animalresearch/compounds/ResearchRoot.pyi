from generated.formats.animalresearch.compounds.ResearchLevel import ResearchLevel
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class ResearchRoot(MemStruct):
    levels: ArrayPointer[ResearchLevel]
    levels_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
