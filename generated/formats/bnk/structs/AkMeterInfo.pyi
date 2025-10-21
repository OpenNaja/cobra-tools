from generated.base_struct import BaseStruct


class AkMeterInfo(BaseStruct):
    f_grid_period: float
    f_grid_offset: float
    f_tempo: float
    u_time_sig_num_beats_bar: int
    u_time_sig_beat_value: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
