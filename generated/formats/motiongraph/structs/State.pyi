from generated.formats.motiongraph.structs.ActivityReference import ActivityReference
from generated.formats.motiongraph.structs.TransStruct import TransStruct
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class State(MemStruct):
    unk: int
    num_activities: int
    activities: ArrayPointer[ActivityReference]
    array_2_count: int
    array_2: ArrayPointer[TransStruct]
    id: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
