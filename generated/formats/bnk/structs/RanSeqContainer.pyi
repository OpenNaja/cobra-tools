from generated.array import Array
from generated.formats.bnk.structs.AkPlaylistItem import AkPlaylistItem
from generated.formats.bnk.structs.HircObject import HircObject
from generated.formats.bnk.structs.NodeBaseParams import NodeBaseParams


class RanSeqContainer(HircObject):
    node_base_params: NodeBaseParams
    s_loop_count: int
    s_loop_mod_min: int
    s_loop_mod_max: int
    f_transition_time: float
    f_transition_time_mod_min: float
    f_transition_time_mod_max: float
    w_avoid_repeat_count: int
    e_transition_mode: int
    e_random_mode: int
    e_mode: int
    by_bit_vector: int
    num_children: int
    children: Array[int]
    num_play_list_item: int
    play_list_item: Array[AkPlaylistItem]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
