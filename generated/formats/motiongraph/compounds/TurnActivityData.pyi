from generated.formats.motiongraph.bitstructs.TurnFlags import TurnFlags
from generated.formats.motiongraph.compounds.DataStreamResourceDataList import DataStreamResourceDataList
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TurnActivityData(MemStruct):
    spot_animation: Pointer[str]
    half_animation: Pointer[str]
    full_animation: Pointer[str]
    output_prop_through_variable: Pointer[str]
    spot_data_streams: DataStreamResourceDataList
    half_data_streams: DataStreamResourceDataList
    full_data_streams: DataStreamResourceDataList
    suppress_resource_data_streams: int
    _pad_0: int
    priorities: int
    lead_out_time: float
    flags: TurnFlags
    _pad_1: int
    _pad_2: int
    max_angle: float
    min_cycles: int
    playback_rate: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
