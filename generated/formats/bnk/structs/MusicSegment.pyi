from generated.array import Array
from generated.formats.bnk.structs.AkMusicMarkerWwise import AkMusicMarkerWwise
from generated.formats.bnk.structs.HircObject import HircObject
from generated.formats.bnk.structs.MusicNodeParams import MusicNodeParams


class MusicSegment(HircObject):
    music_node_params: MusicNodeParams
    f_duration: float
    ul_num_markers: int
    markers: Array[AkMusicMarkerWwise]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
