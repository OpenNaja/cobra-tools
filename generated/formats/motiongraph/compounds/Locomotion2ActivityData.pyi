from generated.formats.motiongraph.compounds.DataStreamResourceDataList import DataStreamResourceDataList
from generated.formats.motiongraph.compounds.Locomotion2AnimationInfo import Locomotion2AnimationInfo
from generated.formats.motiongraph.compounds.Locomotion2BlendSpace import Locomotion2BlendSpace
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Locomotion2ActivityData(MemStruct):
    animation_count: int
    animations: ArrayPointer[Locomotion2AnimationInfo]
    flags: int
    stopping_distance: float
    strafe_turn_blend: float
    turn_blend_limit: float
    turn_speed_multiplier: float
    flex_speed_multiplier: float
    blend_space: Locomotion2BlendSpace
    output_prop_through_variable: Pointer[str]
    speed_variable: Pointer[str]
    orientation_variable: Pointer[str]
    data_streams_count: int
    data_streams: ArrayPointer[DataStreamResourceDataList]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
