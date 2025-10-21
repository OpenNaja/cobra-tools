from generated.formats.motiongraph.bitstructs.AnimationFlags import AnimationFlags
from generated.formats.motiongraph.compounds.DataStreamResourceDataList import DataStreamResourceDataList
from generated.formats.motiongraph.compounds.FloatInputData import FloatInputData
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class AnimationActivityData(MemStruct):
    mani: Pointer[str]
    animation_flags: AnimationFlags
    priorities: int
    weight: FloatInputData
    speed: FloatInputData
    starting_prop_through: float
    lead_out_time: float
    sync_prop_through_variable: Pointer[str]
    count_6: int
    output_prop_through_variable: Pointer[str]
    additional_data_streams: DataStreamResourceDataList

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
