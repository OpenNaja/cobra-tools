from generated.formats.animalresearch.structs.ResearchLevel import ResearchLevel
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class ResearchRoot(MemStruct):
    levels: ArrayPointer[ResearchLevel]
    levels_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
