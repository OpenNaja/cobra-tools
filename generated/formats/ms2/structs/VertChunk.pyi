from typing import Union
from generated.base_struct import BaseStruct
from generated.formats.ms2.bitfields.WeightsFlag import WeightsFlag
from generated.formats.ms2.bitfields.WeightsFlagMalta import WeightsFlagMalta
from generated.formats.ms2.bitfields.WeightsFlagPC2 import WeightsFlagPC2


class VertChunk(BaseStruct):
    precision: float
    pack_base: float
    vertex_offset: int
    vertex_count: int
    weights_flag: Union[WeightsFlag, WeightsFlagMalta, WeightsFlagPC2]
    zero: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
