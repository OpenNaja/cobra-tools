from generated.array import Array
from generated.formats.bani.structs.BaniBones import BaniBones
from generated.formats.bani.structs.BaniData import BaniData
from generated.formats.bani.structs.Keys import Keys
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.ForEachPointer import ForEachPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class BanisRoot(MemStruct):
    bani_data: ArrayPointer[BaniData]
    bones_foreach_bani_data: ForEachPointer[BaniBones]
    bones_2_foreach_bani_data: ForEachPointer[BaniBones]
    keys: Pointer[Keys]
    zeros: Array[int]
    count_a: int
    count_b_0: int
    count_b_1: int
    keys_size: int
    zeros: Array[int]
    bytes_per_frame: int
    bytes_per_bone: int
    num_frames: int
    num_bones: int
    loc_scale: float
    loc_min: float
    bani_count: int
    zero_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
