from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.PadAlign import PadAlign
from generated.formats.manis.structs.CompressedPointer import CompressedPointer
from generated.formats.ovl_base.structs.Empty import Empty


class CompressedHeader(BaseStruct):
    ref: Empty
    size: int
    u_0: int
    u_1: int
    u_2: int
    u_3: int
    const_0: int
    const_1: int
    const_2: int
    const_3: int
    a: int
    b: int
    unk_count: int
    d: int
    e: int
    mani_count: int
    g: int
    h: int
    unka: int
    unkb: int
    minus_1: int
    x: int
    y: int
    pointers_1: Array[CompressedPointer]
    pointers_2: Array[CompressedPointer]
    pad: PadAlign[object]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
