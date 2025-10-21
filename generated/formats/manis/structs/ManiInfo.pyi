from typing import Union
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.PadAlign import PadAlign
from generated.formats.manis.bitfields.ManisDtype import ManisDtype
from generated.formats.manis.bitfields.ManisDtypePC2 import ManisDtypePC2
from generated.formats.ovl_base.structs.Empty import Empty


class ManiInfo(BaseStruct):
    ref: Empty
    duration: float
    frame_count: int
    dtype: Union[ManisDtype, ManisDtypePC2]
    zeros_0: Array[int]
    extra_pc_1: int
    pos_bone_count: int
    ori_bone_count: int
    scl_bone_count: int
    unk_count_0: int
    unk_count_1: int
    unk_count_2: int
    extra_count: int
    float_count: int
    pos_bone_count_repeat: int
    ori_bone_count_repeat: int
    scl_bone_count_repeat: int
    unk_0: int
    unk_1: int
    root_pos_bone: int
    root_ori_bone: int
    target_bone_count: int
    unk_2: int
    unk_3: int
    unk_4: int
    unk_5: int
    extra_zeros_pc: Array[int]
    unk_5: int
    unk_6: int
    unk_7: int
    unk_8: int
    pointers: Array[int]
    extra_for_use_ushort: Array[int]
    pos_bone_min: int
    pos_bone_max: int
    ori_bone_min: int
    ori_bone_max: int
    scl_bone_min: int
    scl_bone_max: int
    pos_bone_count_related: int
    pos_bone_count_repeat: int
    ori_bone_count_related: int
    ori_bone_count_repeat: int
    scl_bone_count_related: int
    scl_bone_count_repeat: int
    zero_0_end: int
    zero_1_end: int
    pad_2: PadAlign[object]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
