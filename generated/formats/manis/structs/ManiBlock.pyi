from typing import Generic, TypeVar, Union
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.PadAlign import PadAlign
from generated.formats.manis.structs.CompressedManiData import CompressedManiData
from generated.formats.manis.structs.CompressedManiDataPC2 import CompressedManiDataPC2
from generated.formats.manis.structs.LimbTrackData import LimbTrackData
from generated.formats.manis.structs.LimbTrackDataZT import LimbTrackDataZT
from generated.formats.manis.structs.UncompressedManiDataPC2 import UncompressedManiDataPC2
from generated.formats.manis.structs.UshortLut import UshortLut
from generated.formats.manis.structs.WarExtra import WarExtra
from generated.formats.ovl_base.structs.Empty import Empty


_T = TypeVar("_T")

class ManiBlock(BaseStruct, Generic[_T]):
    ref: Empty
    pos_bones_names: Array[int]
    ori_bones_names: Array[int]
    scl_bones_names: Array[int]
    floats_names: Array[int]
    pos_channel_to_bone: Array[_T]
    ori_channel_to_bone: Array[_T]
    scl_channel_to_bone: Array[_T]
    pos_bone_to_channel: Array[_T]
    ori_bone_to_channel: Array[_T]
    scl_bone_to_channel: Array[_T]
    pad: PadAlign[object]
    ushort_lut: UshortLut
    start_keys_ref: Empty
    pos_bones: Array[Array[Array[float]]]
    ori_bones: Array[Array[Array[float]]]
    shr_bones: Array[Array[Array[float]]]
    scl_bones: Array[Array[Array[float]]]
    floats: Array[Array[float]]
    uncompressed_pad_pc_2: PadAlign[object]
    precompressed: UncompressedManiDataPC2
    uncompressed_pad: PadAlign[object]
    extra_war: WarExtra
    compressed: Union[CompressedManiData, CompressedManiDataPC2]
    limb_track_data: Union[LimbTrackData, LimbTrackDataZT]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
