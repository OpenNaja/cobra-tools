from generated.formats.cinematic.compounds.State import State
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class CinematicData(MemStruct):
    default_name: Pointer[str]
    next_levels: ArrayPointer[State]
    next_level_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
