from generated.formats.motiongraph.structs.MotiongraphVar import MotiongraphVar
from generated.formats.motiongraph.structs.Transition import Transition
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class MotiongraphVars(MemStruct):
    ptr: ArrayPointer[MotiongraphVar]
    count: int
    transition: Transition

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
