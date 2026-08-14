from typing import Union
from generated.array import Array
from generated.formats.bani.structs.BaniGpuAnimHeader import BaniGpuAnimHeader
from generated.formats.bani.structs.BaniGpuChannels import BaniGpuChannels
from generated.formats.bani.structs.BaniGpuChannelsLod import BaniGpuChannelsLod
from generated.formats.bani.structs.BaniGpuChannelsLod256 import BaniGpuChannelsLod256
from generated.formats.bani.structs.BaniKeys import BaniKeys
from generated.formats.bani.structs.QuantizationInfo import QuantizationInfo
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.ForEachPointer import ForEachPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class BanisRoot(MemStruct):
    gpu_anim_headers: ArrayPointer[BaniGpuAnimHeader]
    channel_bones: ForEachPointer[BaniGpuChannels]
    channel_bones_lod: Union[ForEachPointer[BaniGpuChannelsLod256], ForEachPointer[BaniGpuChannelsLod]]
    keys: Pointer[BaniKeys]
    zeros: Array[int]
    gpu_anim_headers_size: int
    channel_bones_size: int
    channel_bones_lod_size: int
    keys_size: int
    zeros: Array[int]
    bytes_per_frame: int
    bytes_per_bone: int
    num_frames: int
    num_bones: int
    quantization_info: QuantizationInfo
    bani_count: int
    zero_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
