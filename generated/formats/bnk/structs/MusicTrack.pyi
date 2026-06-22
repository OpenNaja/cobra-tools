from generated.array import Array
from generated.formats.bnk.structs.AkBankSourceData import AkBankSourceData
from generated.formats.bnk.structs.AkClipAutomation import AkClipAutomation
from generated.formats.bnk.structs.AkTrackSrcInfo import AkTrackSrcInfo
from generated.formats.bnk.structs.HircObject import HircObject
from generated.formats.bnk.structs.NodeBaseParams import NodeBaseParams
from generated.formats.bnk.structs.SwitchParams import SwitchParams
from generated.formats.bnk.structs.TransParams import TransParams


class MusicTrack(HircObject):
    u_flags: int
    num_sources: int
    ak_bank_source_data: Array[AkBankSourceData]
    num_playlist_item: int
    p_playlist: Array[AkTrackSrcInfo]
    num_sub_track: int
    num_clip_automation_item: int
    p_items: Array[AkClipAutomation]
    node_base_params: NodeBaseParams
    e_track_type: int
    switch_params: SwitchParams
    trans_params: TransParams
    i_look_ahead_time: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
