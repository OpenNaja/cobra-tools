from generated.formats.mechanicresearch.structs.Research import Research
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class ResearchRoot(MemStruct):
    levels: ArrayPointer[Research]
    count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
