from generated.array import Array
from generated.formats.bnk.structs.AkMusicTransitionRule import AkMusicTransitionRule
from generated.formats.bnk.structs.HircObject import HircObject
from generated.formats.bnk.structs.MusicNodeParams import MusicNodeParams


class MusicSwitch(HircObject):
    music_node_params: MusicNodeParams
    num_rules: int
    rules: Array[AkMusicTransitionRule]
    b_is_continue_playback: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
