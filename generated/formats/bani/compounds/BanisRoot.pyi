from generated.array import Array
from generated.formats.bani.compounds.BaniBones import BaniBones
from generated.formats.bani.compounds.BaniData import BaniData
from generated.formats.bani.compounds.Keys import Keys
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.ForEachPointer import ForEachPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


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
