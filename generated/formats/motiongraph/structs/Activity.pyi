from generated.formats.motiongraph.structs.ActivityReference import ActivityReference
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class Activity(MemStruct):
    data_type: Pointer[str]
    data: Pointer[object]
    num_sub_activities: int
    num_other_activities: int
    sub_activities: ArrayPointer[ActivityReference]
    index_a: int
    index_b: int
    other_activities: ArrayPointer[ActivityReference]
    name_b: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
