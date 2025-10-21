from generated.base_struct import BaseStruct
from generated.formats.bnk.bitfields.UBitsPositioning import UBitsPositioning
from generated.formats.bnk.structs.PositioningData import PositioningData


class PositioningParams(BaseStruct):
    u_bits_positioning: UBitsPositioning
    positioning_data: PositioningData

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
