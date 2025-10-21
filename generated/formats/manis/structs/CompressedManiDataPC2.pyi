from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.structs.SmallChunk import SmallChunk
from generated.formats.ovl_base.structs.Empty import Empty


class CompressedManiDataPC2(BaseStruct):
    size: int
    ref: Empty
    u_0: int
    constant: Array[int]
    bone_count: int
    frame_count: int
    fps: float
    unk_float: float
    frame_segments_count: int
    u_3: int
    ori_bone_count: int
    pos_bone_count: int
    scl_bone_count: int
    morph_bone_count: int
    unk_count_1: int
    unk_count_2: int
    unk_count_3: int
    ff: int
    count: int
    s_1: int
    s_2: int
    s_3: int
    frame_segments: Array[int]
    ff_2: int
    chunks: Array[SmallChunk]
    ref_2: Empty
    databytes: Array[int]
    ref_3: Empty

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
