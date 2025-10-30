from generated.base_struct import BaseStruct
from generated.formats.bnk.structs.FadeParams import FadeParams


class AkMusicTransitionObject(BaseStruct):
    segment_i_d: int
    fade_in_params: FadeParams
    fade_out_params: FadeParams
    b_play_pre_entry: int
    b_play_post_exit: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
