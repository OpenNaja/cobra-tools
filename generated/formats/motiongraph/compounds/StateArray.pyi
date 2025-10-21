from generated.formats.motiongraph.compounds.StateReference import StateReference
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class StateArray(MemStruct):
    states_count: int
    states: ArrayPointer[StateReference]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
