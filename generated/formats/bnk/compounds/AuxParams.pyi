from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.bitfields.AuxBitfield import AuxBitfield


class AuxParams(BaseStruct):
    by_bit_vector: AuxBitfield
    aux: Array[int]
    reflections_aux_bus: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
