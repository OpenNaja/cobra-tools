from generated.array import Array
from generated.formats.motiongraph.compounds.RandomActivityActivityInfo import RandomActivityActivityInfo
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class RandomSelectActivityActivityData(MemStruct):
    activities: ArrayPointer[RandomActivityActivityInfo]
    num_activities: int
    blend_in_time: float
    blend_out_time: float
    allow_restarting_activity: int
    _pad_allow_restarting_activity: Array[int]
    block_activity_restart_time: float
    random_animation_flags: int
    always_active: int
    _pad_always_active: Array[int]
    min_gap: float
    max_gap: float
    _max_gap_pad: int
    random_number_var: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
