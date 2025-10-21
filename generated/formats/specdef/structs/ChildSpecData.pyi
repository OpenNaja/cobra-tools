from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.specdef.structs.SpecdefPointer import SpecdefPointer
from generated.formats.specdef.structs.SpecdefRoot import SpecdefRoot


class ChildSpecData(MemStruct):
    specdef: SpecdefPointer[SpecdefRoot]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
