from generated.formats.motiongraph.structs.Activity import Activity
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class TriggeredActivityActivityData(MemStruct):
    trigger: Pointer[str]
    activity: Pointer[Activity]
    blend_in_time: float
    blend_out_time: float
    m_auto_start: int
    m_allow_restart: int
    m_allow_mortal: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
