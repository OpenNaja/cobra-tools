from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.enums.AkPropID import AkPropID
from generated.formats.bnk.structs.AkPropMinMax import AkPropMinMax


class NodeInitialParams(BaseStruct):
    c_props_1: int
    p_props_1: Array[AkPropID]
    p_values_1: Array[float]
    c_props_2: int
    p_props_2: Array[AkPropMinMax]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
