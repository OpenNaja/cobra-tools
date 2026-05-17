from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.PadAlign import PadAlign
from generated.formats.base.structs.ZStringBuffer import ZStringBuffer
from generated.formats.landscape.structs.Pass import Pass
from generated.formats.landscape.structs.Struct0 import Struct0


class Buffer0(BaseStruct):
    names: ZStringBuffer
    names_padding: PadAlign[object]
    floats: Array[float]
    stuff: Array[int]
    name_offsets: Array[int]
    unk: Array[int]
    passes: Array[Pass]
    unk_2: Array[int]
    vecs: Array[Array[float]]
    unk_3: Array[int]
    unk_4: Array[Struct0]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
