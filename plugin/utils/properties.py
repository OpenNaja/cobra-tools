import sys

import bpy.props
from bpy.props import IntProperty, EnumProperty
from bpy.types import PropertyGroup

from generated.formats.ms2.enums.Jwe1Collision import Jwe1Collision
from generated.formats.ms2.enums.Jwe1Surface import Jwe1Surface
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


class_jwe = [e.name for e in Jwe1Collision]
class_pz = ['Animal', 'Animal_Bone', 'Animal_Box', 'Animal_Dead', 'Animal_Pouncing', 'Balloon', 'Bedding', 'Building', 'Character_InFlight', 'Character_Limb', 'Character_Limb_NoCollision', 'Character_Miscreant', 'Character_SoS', 'Climbable', 'Coaster', 'Coaster_Car', 'Coaster_Misc', 'Coaster_RacingCar', 'DevelopmentOnly_Ball', 'DevelopmentOnly_Character', 'Enrichment_Object', 'Facility', 'Kinetic_Object', 'Landscape', 'Navmesh', 'NoCollision', 'Poo', 'Prop', 'Ride', 'Scenery', 'Scenery_NoNavSource', 'Scenery_Vandalised', 'Structure', 'Track', 'TrackScenery', 'Track_Support', 'TreeBase', 'TreeBranch', 'TreeFoliage', 'TreeTrunk', 'Trigger_AnimalMemorialStaffThoughts', 'Trigger_AnimalObstruction', 'Trigger_EducationSource', 'Trigger_EscapedAnimal', 'Trigger_FacilityNegativeInfluence', 'Trigger_Grid', 'Trigger_GuestGate', 'Trigger_Inspector', 'Trigger_Presenter', 'Trigger_Queue', 'Trigger_Screen', 'Trigger_Security', 'UIElement', 'Water', 'WaterSpray', 'Wheel']
class_jwe2 = ['AIDrone', 'AIVehicle', 'AIVehicleFindGrid', 'AIVehicleObstacle', 'Audio', 'AviaryTourGate', 'Building', 'BuildingAIVehicleObstacle', 'BuildingNoCameraObstacle', 'CameraObstacle', 'CarBody', 'CarObstacle', 'Character', 'Debris', 'Default', 'Development', 'DevelopmentAll', 'Dinosaur', 'DinosaurCollisionProxy', 'DinosaurDinosaur', 'DinosaurNoBuilding', 'DinosaurNoCollision', 'DinosaurNoFence', 'DinosaurNoVehicle', 'DinosaurSelfCollision', 'Drone', 'Fence', 'FlyingVehicleObstacle', 'Foliage', 'Gate', 'Guest', 'GuestAvoidance', 'GuestObstacle', 'GuestRagdoll', 'HatcheryGate', 'InvisibleWall', 'LEGACY_DO_NOT_USE', 'LagoonFloor', 'Landscape', 'MissionTrigger', 'PaleoFoodPoint', 'Path', 'Perch', 'PerchQuetz', 'Prop', 'PropNoCameraObstacle', 'Pylon', 'Rotor', 'TinyDinosaurCollisionProxy', 'TourGate', 'Track', 'Tree', 'Vehicle', 'Wall', 'Water', 'WaterSplash', 'Wheel']
surfaces_jwe = [e.name for e in Jwe1Surface]
surfaces_pz = ['Animal', 'Brick', 'Character', 'Cloth', 'Concrete', 'Default', 'Default_Legacy_DO_NOT_USE', 'Dirt', 'Foliage', 'Frictionless', 'Glass', 'Grass', 'Ice', 'Leaves', 'Litter', 'Metal', 'Mud', 'Plastic', 'Poo', 'Rubber', 'Sand', 'Snow', 'Stone', 'Tree', 'Trigger', 'Tyre', 'Wood']
surfaces_jwe2 = ['BuildingBrick', 'BuildingConcrete', 'BuildingGlass', 'BuildingIce', 'BuildingMetal', 'BuildingSnow', 'BuildingWood', 'CarBody', 'CharacterCollidableLimb', 'CharacterFlying', 'CharacterNonCollidableLimb', 'Debris', 'Default', 'DinosaurLimb', 'DirtPath', 'Drone', 'Gyrosphere', 'LEGACY_DO_NOT_USE', 'LagoonFloor', 'LandscapeDefault', 'LandscapeDirt', 'LandscapeFoliage', 'LandscapeFrictionless', 'LandscapeGrass', 'LandscapeIce', 'LandscapeMetal', 'LandscapeMud', 'LandscapePondBottom', 'LandscapeSand', 'LandscapeSnow', 'LandscapeStone', 'LandscapeWood', 'LandscapeWoodHollow', 'NonCollidableLimb', 'PaleoFoodPoint', 'PropLeaves', 'PropLitter', 'PropMetal', 'PropPlastic', 'PropStone', 'PropTree', 'PropWooden', 'SceneryDefault', 'SceneryTree', 'StructureFence', 'StructurePath', 'StructurePylon', 'StructureTrack', 'StructureWall', 'Water']


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
    classification_jwe: EnumProperty(
        name='Classification',
        description='Hitcheck Classification Name for Jurassic World Evolution',
        items=[(name, name, "") for name in class_jwe],
    )
    classification_pz: EnumProperty(
        name='Classification',
        description='Hitcheck Classification Name for Planet Zoo',
        items=[(name, name, "") for name in class_pz],
    )
    classification_jwe2: EnumProperty(
        name='Classification',
        description='Hitcheck Classification Name for Jurassic World Evolution 2',
        items=[(name, name, "") for name in class_jwe2],
    )
    surface_jwe: EnumProperty(
        name='Surface',
        description='Hitcheck Surface Name for Jurassic World Evolution',
        items=[(name, name, "") for name in surfaces_jwe],
    )
    surface_pz: EnumProperty(
        name='Surface',
        description='Hitcheck Surface Name for Planet Zoo',
        items=[(name, name, "") for name in surfaces_pz],
    )
    surface_jwe2: EnumProperty(
        name='Surface',
        description='Hitcheck Surface Name for Jurassic World Evolution 2',
        items=[(name, name, "") for name in surfaces_jwe2],
    )
