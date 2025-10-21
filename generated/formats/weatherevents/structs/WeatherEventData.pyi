from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class WeatherEventData(MemStruct):
    event_name: Pointer[str]
    float_1: float
    float_2: float
    float_3: float
    float_4: float
    float_5: float
    float_6: float
    float_7: float
    float_8: float
    float_9: float
    float_10: float
    event_curve_name_from_base: Pointer[str]
    unk_1_as_1: int
    float_11: float
    float_12: float
    float_13: float
    float_14: float
    float_15: float
    event_curve_clouds: Pointer[str]
    block_1_unk_as_1: int
    block_1_float_1: float
    block_1_float_2: float
    block_1_float_3: float
    block_1_float_4: float
    block_1_float_5: float
    block_1_float_6: float
    block_1_float_7: float
    block_2_unk_as_1: int
    block_2_float_1: float
    block_2_float_2: float
    block_2_float_3: float
    block_2_float_4: float
    block_2_float_5: float
    block_2_float_6: float
    block_2_float_7: float
    block_3_unk_as_1: int
    block_3_float_1: float
    block_3_float_2: float
    block_3_float_3: float
    block_3_float_4: float
    block_3_float_5: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
