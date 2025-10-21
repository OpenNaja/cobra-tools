from generated.bitfield import BasicBitfield


class RagdollPhysicsActivityFlags(BasicBitfield):
    auto_sleep_enabled: int
    collision_enabled: int
    spatial_enabled: int
    motor_driving_enabled: int
    constraint_projection: int
    activate_on_startup: int
    activate_on_collision: int
    activate_one_time_only: int
    activate_by_data_stream: int
    wake_on_activation: int
    activation_disabled: int
    lock_pose_on_activation: int
    deactivate_pose_match: int
    motor_pose_matching: int
    motor_joint_stiffening: int
    force_sub_step_synch: int
    force_disable_synch: int
    force_callbacks: int
