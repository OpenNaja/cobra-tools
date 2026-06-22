from typing import Union
from generated.base_struct import BaseStruct
from generated.formats.bnk.bitfields.UBitsPositioning import UBitsPositioning
from generated.formats.bnk.bitfields.UBitsPositioning122 import UBitsPositioning122
from generated.formats.bnk.structs.PositioningAutomation import PositioningAutomation


class PositioningParams(BaseStruct):
    u_bits_positioning: Union[UBitsPositioning, UBitsPositioning122]
    u_bits_3_d: int
    positioning_automation: PositioningAutomation
    u_attenuation_i_d: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
