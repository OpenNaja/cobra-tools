from typing import Union
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.PadAlign import PadAlign
from generated.formats.ms2.structs.Bone import Bone
from generated.formats.ms2.structs.BonePointer import BonePointer
from generated.formats.ms2.structs.IKInfo import IKInfo
from generated.formats.ms2.structs.JointData import JointData
from generated.formats.ms2.structs.Matrix44 import Matrix44
from generated.formats.ms2.structs.MinusPadding import MinusPadding
from generated.formats.ms2.structs.ZerosPadding import ZerosPadding
from generated.formats.ovl_base.structs.Empty import Empty


class BoneInfo(BaseStruct):
    name_count: int
    z_0: int
    inv_names_count: int
    bone_limits: Array[BonePointer]
    zero_0: int
    unknown_0_c: int
    unk_count: int
    unk_unused: int
    war_a: int
    bone_limits: Array[BonePointer]
    war_b: int
    bind_matrix_count: int
    zeros: Array[int]
    inv_data_count: int
    bone_count: int
    unknown_40: int
    parents_count: int
    extra_zero: int
    enum_count: int
    unknown_58: int
    one: int
    one_1_jwe_3: int
    one_2_jwe_3: int
    unk_pc_count: int
    zeros_count: int
    ik_count: int
    joint_count: int
    zero_1: int
    zero_2: int
    zero_3: int
    names_ref: Empty
    name_indices: Array[int]
    inventory_name_indices: Array[int]
    name_padding: PadAlign[object]
    inverse_bind_matrices: Array[Matrix44]
    bones: Array[Bone]
    parents: Array[int]
    enumeration: Array[int]
    jwe_3_a: Array[int]
    parents_padding: PadAlign[object]
    enumeration: Union[Array[Array[int]], Array[int]]
    inventory_datas: Array[Array[int]]
    weirdness: Array[int]
    inventory_datas_2: Array[Array[int]]
    minus_padding: MinusPadding
    zeros_padding: ZerosPadding
    ik_info: IKInfo
    joints: JointData

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
