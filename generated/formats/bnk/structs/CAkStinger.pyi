from generated.base_struct import BaseStruct


class CAkStinger(BaseStruct):
    trigger_i_d: int
    segment_i_d: int
    sync_play_at: int
    u_cue_filter_hash: int
    dont_repeat_time: int
    num_segment_look_ahead: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
