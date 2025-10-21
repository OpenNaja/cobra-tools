import numpy as np
from generated.array import Array
from generated.formats.bani.structs.BoneInfo import BoneInfo
from generated.formats.base.structs.PadAlign import PadAlign
from generated.formats.ovl_base.structs.Empty import Empty
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class BaniBones(MemStruct):
    ref: Empty
    data: np.ndarray[tuple[int], np.dtype[BoneInfo]]
    padding: PadAlign[object]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
