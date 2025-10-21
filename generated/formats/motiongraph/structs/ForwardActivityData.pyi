from generated.formats.motiongraph.enums.UseValueType import UseValueType
from generated.formats.motiongraph.structs.DataStreamResourceDataList import DataStreamResourceDataList
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class ForwardActivityData(MemStruct):
    straight_forward_animation: Pointer[str]
    left_forward_animation: Pointer[str]
    right_forward_animation: Pointer[str]
    straight_spot_animation: Pointer[str]
    output_prop_through_variable: Pointer[str]
    cycled_variable: Pointer[str]
    straight_forward_data_streams: DataStreamResourceDataList
    left_forward_data_streams: DataStreamResourceDataList
    right_forward_data_streams: DataStreamResourceDataList
    straight_spot_data_streams: DataStreamResourceDataList
    forward_flags: int
    suppress_resource_data_streams: int
    priorities: int
    turn_radius: float
    turn_radius_value_type: UseValueType
    _pad_0: int
    stride_length: float
    stride_length_value_type: UseValueType
    _pad_1: int
    lead_out_time: float
    anticipation_distance: float
    unfused_cycles: int
    cycle_count: int
    repeat_count: int
    min_cycles: int
    playback_rate: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
