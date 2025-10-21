from generated.formats.motiongraph.bitstructs.RagdollPhysicsActivityFlags import RagdollPhysicsActivityFlags
from generated.formats.motiongraph.compounds.FloatInputData import FloatInputData
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class RagdollPhysicsActivityData(MemStruct):
    weight: FloatInputData
    flag: RagdollPhysicsActivityFlags
    _flag_pad: int
    root_bone_name: Pointer[str]
    collision_exclude_mask: int
    collision_exclude_0: Pointer[str]
    collision_exclude_1: Pointer[str]
    collision_exclude_2: Pointer[str]
    collision_exclude_3: Pointer[str]
    collision_exclude_4: Pointer[str]
    collision_exclude_5: Pointer[str]
    collision_exclude_6: Pointer[str]
    collision_exclude_7: Pointer[str]
    min_motor_driving_force: float
    max_motor_driving_force: float
    motor_weight_variable: Pointer[str]
    pose_match_lin_threshold: float
    pose_match_ang_threshold: float
    bone_chain_priority: int
    data_stream_name: Pointer[str]
    data_stream_type: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
