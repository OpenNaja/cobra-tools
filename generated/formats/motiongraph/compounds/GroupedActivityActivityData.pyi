from generated.formats.motiongraph.compounds.ActivityReference import ActivityReference
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class GroupedActivityActivityData(MemStruct):
    activities: ArrayPointer[ActivityReference]
    num_activities: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
