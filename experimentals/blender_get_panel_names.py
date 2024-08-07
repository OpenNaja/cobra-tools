# get panel names
import bpy

for panel in bpy.types.Panel.__subclasses__():
    print(panel.__name__)
# PHYSICS_PT_rigid_body
# PHYSICS_PT_rigid_body_settings
# PHYSICS_PT_rigid_body_collisions
# PHYSICS_PT_rigid_body_collisions_surface
# PHYSICS_PT_rigid_body_collisions_sensitivity
# PHYSICS_PT_rigid_body_collisions_collections
# PHYSICS_PT_rigid_body_dynamics
# PHYSICS_PT_rigid_body_dynamics_deactivation
# PHYSICS_PT_rigid_body_constraint
# PHYSICS_PT_rigid_body_constraint_settings
# PHYSICS_PT_rigid_body_constraint_objects
# PHYSICS_PT_rigid_body_constraint_override_iterations
# PHYSICS_PT_rigid_body_constraint_limits
# PHYSICS_PT_rigid_body_constraint_limits_linear
# PHYSICS_PT_rigid_body_constraint_limits_angular
# PHYSICS_PT_rigid_body_constraint_motor
# PHYSICS_PT_rigid_body_constraint_motor_angular
# PHYSICS_PT_rigid_body_constraint_motor_linear
# PHYSICS_PT_rigid_body_constraint_springs
# PHYSICS_PT_rigid_body_constraint_springs_angular
# PHYSICS_PT_rigid_body_constraint_springs_linear