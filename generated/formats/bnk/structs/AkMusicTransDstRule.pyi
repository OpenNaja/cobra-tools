from generated.base_struct import BaseStruct
from generated.formats.bnk.structs.FadeParams import FadeParams


class AkMusicTransDstRule(BaseStruct):
    fade_params: FadeParams
    u_cue_filter_hash: int
    u_jump_to_i_d: int
    e_jump_to_type: int
    e_entry_type: int
    b_play_pre_entry: int
    b_dest_match_source_cue_name: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
