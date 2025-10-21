from generated.formats.motiongraph.compounds.MotiongraphVar import MotiongraphVar
from generated.formats.motiongraph.compounds.Transition import Transition
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class MotiongraphVars(MemStruct):
    ptr: ArrayPointer[MotiongraphVar]
    count: int
    transition: Transition

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
