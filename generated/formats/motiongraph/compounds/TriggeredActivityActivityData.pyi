from generated.formats.motiongraph.compounds.Activity import Activity
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TriggeredActivityActivityData(MemStruct):
    trigger: Pointer[str]
    activity: Pointer[Activity]
    blend_in_time: float
    blend_out_time: float
    m_auto_start: int
    m_allow_restart: int
    m_allow_mortal: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
