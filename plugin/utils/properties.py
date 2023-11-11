import sys

import bpy.props
from bpy.props import IntProperty, EnumProperty
from bpy.types import PropertyGroup

from generated.formats.ms2.enums.MeshFormat import MeshFormat
from generated.formats.ms2.enums.RigidBodyFlag import RigidBodyFlag


class CobraSceneSettings(PropertyGroup):
    num_streams: IntProperty(
        name="External Streams",
        description="Number of lod levels stored in external .modelstream files",
        default=0,
        min=0,
        max=6
    )
    version: IntProperty(
        name="MS2 Version",
        description="Version to use for export",
        default=50,
        min=0,
        max=100
    )


class CobraMeshSettings(PropertyGroup):
    mesh_format: EnumProperty(
        name='Mesh Format',
        description='Mesh format used for this mesh - JWE2 after Biosyn update',
        items=[("NONE", "None", "")] + [(item.name, item.name, "") for i, item in enumerate(MeshFormat)],
        # default = 'MO_SYS_FIXED',

    )


class CobraCollisionSettings(PropertyGroup):
    air_resistance: bpy.props.FloatVectorProperty(
        name='Air Resistance',
        description="Air Resistance in 3D, relative to the joint's axes",
        default=(0.0, 0.0, 0.0),
        min=sys.float_info.min,
        max=sys.float_info.max,
        soft_min=sys.float_info.min,
        soft_max=sys.float_info.max,
        step=3,
        precision=2,
        subtype="XYZ")
    damping_3d: bpy.props.FloatVectorProperty(
        name='Damping',
        description='Damping in 3D',
        default=(0.0, 0.0, 0.0),
        min=sys.float_info.min,
        max=sys.float_info.max,
        soft_min=sys.float_info.min,
        soft_max=sys.float_info.max,
        step=1,
        precision=6)
    plasticity_min: bpy.props.FloatProperty(name="Plasticity Lower", subtype="ANGLE")
    plasticity_max: bpy.props.FloatProperty(name="Upper", subtype="ANGLE")
    flag: EnumProperty(
        name='Dynamics Flag',
        description='Current state of this rigidbody',
        items=[(item.name, item.name, "") for i, item in enumerate(RigidBodyFlag)],
    )
