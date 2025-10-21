from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.tex.structs.Mipmap import Mipmap


class SizeInfoRaw(MemStruct):
    zero: int
    data_size: int
    width: int
    height: int
    depth: int
    num_tiles: int
    num_mips: int
    unk_pz: int
    mip_maps: Array[Mipmap]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
