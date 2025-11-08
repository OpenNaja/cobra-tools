from generated.base_struct import BaseStruct
from generated.formats.bnk.structs.FadeParams import FadeParams


class AkMusicTransSrcRule(BaseStruct):
    fade_params: FadeParams
    e_sync_type: int
    u_cue_filter_hash: int
    b_play_post_exit: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
