from typing import Union
from generated.array import Array
from generated.formats.base.compounds.PadAlign import PadAlign
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.Empty import Empty
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.tex.compounds.SizeInfo import SizeInfo
from generated.formats.tex.compounds.TexBuffer import TexBuffer
from generated.formats.tex.compounds.TexBufferPc import TexBufferPc
from generated.formats.tex.enums.DdsType import DdsType
from generated.formats.tex.enums.DdsTypeCoaster import DdsTypeCoaster


class TexHeader(MemStruct):
    zero_0: int
    zero_1: int
    buffer_infos: Union[ArrayPointer[TexBufferPc], ArrayPointer[TexBuffer]]
    size_info: Pointer[SizeInfo]
    compression_type: Union[DdsType, DdsTypeCoaster]
    one_0: int
    num_mips: int
    width: int
    height: int
    stream_count: int
    stream_count_repeat: int
    pad: int
    pad_dla: int
    zero_0: int
    compression_type: DdsType
    compression_pad: Array[int]
    width: int
    height: int
    depth: int
    num_mips: int
    num_tiles: int
    texel_ref: Empty
    texel: str
    texel_padding: PadAlign[object]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
