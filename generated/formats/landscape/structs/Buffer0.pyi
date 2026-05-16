from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.PadAlign import PadAlign
from generated.formats.base.structs.ZStringBuffer import ZStringBuffer


class Buffer0(BaseStruct):
    names: ZStringBuffer
    names_padding: PadAlign[object]
    floats: Array[float]
    stuff: Array[int]
    name_indices: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
