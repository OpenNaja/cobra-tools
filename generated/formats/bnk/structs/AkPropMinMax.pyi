from generated.base_struct import BaseStruct
from generated.formats.bnk.enums.AkPropID import AkPropID


class AkPropMinMax(BaseStruct):
    p_i_d: AkPropID
    min: float
    max: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
