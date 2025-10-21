from generated.formats.motiongraph.compounds.ActivityReference import ActivityReference
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


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
