from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.PadAlign import PadAlign
from generated.formats.base.structs.ZStringBuffer import ZStringBuffer
from generated.formats.landscape.structs.Lod import Lod
from generated.formats.landscape.structs.Pass import Pass
from generated.formats.landscape.structs.Repeat2 import Repeat2
from generated.formats.landscape.structs.RepeatLong import RepeatLong
from generated.formats.landscape.structs.Something import Something
from generated.formats.landscape.structs.Str48 import Str48
from generated.formats.landscape.structs.Struct0 import Struct0


class Buffer0(BaseStruct):
    names_buffer: ZStringBuffer
    names_padding: PadAlign[object]
    floats: Array[float]
    repeat_long_1: Array[RepeatLong]
    lods: Array[Lod]
    stuff: Array[int]
    names: Array[int]
    floats_2: Array[float]
    name: int
    count_1: int
    count_2: int
    count_z_0: int
    count_z_1: int
    count_z_2: int
    count_3: int
    something: Array[Something]
    repeats: Array[RepeatLong]
    floa: Array[Array[float]]
    name_2: int
    count_48: int
    str_48: Array[Str48]
    repeats_2: Array[int]
    count_repeat_2: int
    count_pass: int
    repeats_3: Array[int]
    repeat_2: Array[Repeat2]
    pad: Array[int]
    passes: Array[Pass]
    unk_2: Array[int]
    vecs: Array[Array[float]]
    unk_3: Array[int]
    unk_3_a: int
    unk_3_b: int
    unk_4: Array[Struct0]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
