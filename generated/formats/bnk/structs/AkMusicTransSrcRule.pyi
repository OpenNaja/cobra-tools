from generated.base_struct import BaseStruct


class AkMusicTransSrcRule(BaseStruct):
    transition_time: int
    e_fade_curve: int
    i_fade_offset: int
    e_sync_type: int
    u_cue_filter_hash: int
    b_play_post_exit: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
