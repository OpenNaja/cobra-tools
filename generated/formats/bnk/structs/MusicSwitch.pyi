from generated.array import Array
from generated.formats.bnk.structs.AkGameSync import AkGameSync
from generated.formats.bnk.structs.AkMusicTransitionRule import AkMusicTransitionRule
from generated.formats.bnk.structs.HircObject import HircObject
from generated.formats.bnk.structs.MusicNodeParams import MusicNodeParams


class MusicSwitch(HircObject):
    music_node_params: MusicNodeParams
    num_rules: int
    rules: Array[AkMusicTransitionRule]
    b_is_continue_playback: int
    u_tree_depth: int
    arguments: Array[AkGameSync]
    u_tree_data_size: int
    u_mode: int
    u_tree_data: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
