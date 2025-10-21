from generated.array import Array
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.tex.compounds.Pc2TexMip import Pc2TexMip
from generated.formats.tex.enums.DdsType import DdsType


class Pc2TexBuffer(MemStruct):
    compression_type: DdsType
    compression_pad: Array[int]
    width: int
    height: int
    depth: int
    num_tiles: int
    flag: int
    num_mips: int
    num_mips_low: int
    num_mips_high: int
    weave_width: int
    weave_height: int
    can_weave: int
    buffer_size: int
    main: Array[Pc2TexMip]
    mip_maps: Array[Pc2TexMip]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
