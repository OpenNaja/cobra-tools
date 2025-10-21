from generated.formats.animalresearch.structs.UnlockState import UnlockState
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class ResearchStartRoot(MemStruct):
    states: ArrayPointer[UnlockState]
    states_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
