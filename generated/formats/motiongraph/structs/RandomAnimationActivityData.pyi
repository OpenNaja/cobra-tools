from generated.formats.motiongraph.structs.ActivityAnimationInfo import ActivityAnimationInfo
from generated.formats.motiongraph.structs.DataStreamResourceDataList import DataStreamResourceDataList
from generated.formats.motiongraph.structs.LoopedAnimationInfo import LoopedAnimationInfo
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class RandomAnimationActivityData(MemStruct):
    num_animations: int
    animations: ArrayPointer[ActivityAnimationInfo]
    data_streams_count: int
    data_streams: ArrayPointer[DataStreamResourceDataList]
    num_looped_animations: int
    looped_animations: ArrayPointer[LoopedAnimationInfo]
    looped_data_streams_count: int
    looped_data_streams: ArrayPointer[DataStreamResourceDataList]
    duration: float
    blend_time: float
    min_weight: float
    max_weight: float
    min_gap: float
    max_gap: float
    priorities: int
    random_animation_flags: int
    sync_variable: Pointer[str]
    random_number_variable: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
