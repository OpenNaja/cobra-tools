from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.PadAlign import PadAlign
from generated.formats.base.structs.ZStringBuffer import ZStringBuffer
from generated.formats.ms2.structs.BallConstraint import BallConstraint
from generated.formats.ms2.structs.HingeConstraint import HingeConstraint
from generated.formats.ms2.structs.HitcheckPointerReader import HitcheckPointerReader
from generated.formats.ms2.structs.HitcheckReader import HitcheckReader
from generated.formats.ms2.structs.JointInfo import JointInfo
from generated.formats.ms2.structs.JointTransform import JointTransform
from generated.formats.ms2.structs.RagdollConstraint import RagdollConstraint
from generated.formats.ms2.structs.RigidBody import RigidBody
from generated.formats.ovl_base.structs.Empty import Empty
from generated.formats.ovl_base.structs.SmartPadding import SmartPadding


class JointData(BaseStruct):
    start_pc: SmartPadding
    before_dla_0: int
    before_dla_1: int
    joint_count: int
    num_ball_constraints: int
    num_hinge_constraints: int
    num_ragdoll_constraints: int
    zero_0: int
    zero_1: int
    namespace_length: int
    zeros_0: Array[int]
    pc_count: int
    zeros_1: Array[int]
    extra_zeros_2: Array[int]
    one_0: int
    one_1: int
    bone_count: int
    root_joint_index: int
    zeros_2: Array[int]
    zeros_3: int
    names_ref: Empty
    joint_transforms: Array[JointTransform]
    rigid_body_pointers: Array[int]
    rigid_body_list: Array[RigidBody]
    ball_constraints: Array[BallConstraint]
    hinge_constraints: Array[HingeConstraint]
    ragdoll_constraints: Array[RagdollConstraint]
    joint_infos: Array[JointInfo]
    pc_floats: Array[Array[float]]
    joint_to_bone: Array[int]
    bone_to_joint: Array[int]
    joint_names: ZStringBuffer
    joint_names_padding: PadAlign[object]
    hitcheck_pointer_reader: HitcheckPointerReader
    after_names: SmartPadding
    hitcheck_reader: HitcheckReader
    joint_infos: Array[JointInfo]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
