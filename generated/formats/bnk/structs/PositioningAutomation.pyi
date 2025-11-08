from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.structs.AkPathListItemOffset import AkPathListItemOffset
from generated.formats.bnk.structs.AkPathVertex import AkPathVertex
from generated.formats.bnk.structs.Vec import Vec


class PositioningAutomation(BaseStruct):
    e_path_mode: int
    transition_time: int
    ul_num_vertices: int
    vertices: Array[AkPathVertex]
    ul_num_play_list_item: int
    p_play_list_items: Array[AkPathListItemOffset]
    ak_3_d_automation_params: Array[Vec]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
