from generated.base_struct import BaseStruct


class AkTrackSrcInfo(BaseStruct):
    track_i_d: int
    source_i_d: int
    event_i_d: int
    f_play_at: float
    f_begin_trim_offset: float
    f_end_trim_offset: float
    f_src_duration: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
