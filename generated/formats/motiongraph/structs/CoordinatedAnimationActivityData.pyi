from generated.formats.motiongraph.structs.DataStreamResourceDataList import DataStreamResourceDataList
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class CoordinatedAnimationActivityData(MemStruct):
    coord_group: Pointer[str]
    waiting_anim: Pointer[str]
    waiting_anim_data_streams: DataStreamResourceDataList
    coordinated_anim: Pointer[str]
    coordinated_anim_data_streams: DataStreamResourceDataList
    priorities: int
    looping: int
    _pad: int
    blend_time: float
    output_prop_through_variable: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
