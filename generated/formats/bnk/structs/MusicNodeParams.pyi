from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.structs.AkMeterInfo import AkMeterInfo
from generated.formats.bnk.structs.NodeBaseParams import NodeBaseParams


class MusicNodeParams(BaseStruct):
    u_flags: int
    node_base_params: NodeBaseParams
    ul_num_childs: int
    children: Array[int]
    ak_meter_info: AkMeterInfo
    b_meter_info_flag: int
    num_stingers: int
    stingers: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
