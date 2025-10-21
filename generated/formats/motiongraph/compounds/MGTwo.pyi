from generated.formats.motiongraph.compounds.NestedZStr import NestedZStr
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class MGTwo(MemStruct):
    count: int
    ptr: ArrayPointer[NestedZStr]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
