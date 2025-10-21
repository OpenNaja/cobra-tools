from generated.formats.motiongraph.compounds.ActivityReference import ActivityReference
from generated.formats.motiongraph.enums.SelectActivityActivityMode import SelectActivityActivityMode
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class SelectActivityActivityData(MemStruct):
    enum_variable: Pointer[str]
    activities: ArrayPointer[ActivityReference]
    num_activities: int
    blend_time: float
    mode: SelectActivityActivityMode

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
