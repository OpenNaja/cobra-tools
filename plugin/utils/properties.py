import enum
import sys

import bpy.props
from bpy.props import IntProperty, EnumProperty
from bpy.types import PropertyGroup

from constants import ConstantsProvider
from generated.formats.ms2.enums.Jwe1Collision import Jwe1Collision
from generated.formats.ms2.enums.Jwe1Surface import Jwe1Surface
from generated.formats.ms2.enums.MeshFormat import MeshFormat
from generated.formats.ms2.enums.RigidBodyFlag import RigidBodyFlag


class VersionedPropertyGroup(PropertyGroup):

	def get_current_game_suffix(self, context):
		version = context.scene.cobra.version
		if version in (47, ):
			return "_jwe"
		elif version in (48, 50):
			return "_pz"
		elif version in (51, 52):
			return "_jwe2"

	def get_current_versioned_name(self, context, name):
		return f"{name}{self.get_current_game_suffix(context)}"

	def get_value(self, context, name):
		return getattr(self, self.get_current_versioned_name(context, name))

	def set_value(self, context, name, v):
		if isinstance(v, enum.Enum):
			v = v.name
		return setattr(self, self.get_current_versioned_name(context, name), v)


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


class CobraCollisionSettings(VersionedPropertyGroup):
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


from bpy.props import *
from bpy.types import (Panel, Operator, PropertyGroup, )
import uuid


# region Global variables, functions and properties of Collection for MOD creation
def update_uuid(self, context):
	if self.uuid == "":
		self.uuid = str(uuid.uuid4())
	return


class ModData(PropertyGroup):
	"""Stores enough information to create a mod from this blender file"""
	name: StringProperty(name="Name", description='This is the human-readable name of the mod.')
	desc: StringProperty(name="Description", description="Mod's description is used to create the readme file.")
	game: EnumProperty(name="Game",
					   items=(
						   ('JURASSIC_WORLD_EVOLUTION', 'Jurassic World Evolution', ""),
						   ('JURASSIC_WORLD_EVOLUTION_2', 'Jurassic World Evolution 2', ""),
						   ('PLANET_COASTER', 'Planet Coaster', ""),
						   ('PLANET_ZOO', 'Planet Zoo', "")
					   )
					   )
	uuid: StringProperty(name="UUID", description="Mod's uuid. Delete to generate a new one", update=update_uuid, )
	ordid: IntProperty(name="Order ID",
					   description="Mod's starting id for to assets (Use a free Id). IDs will be assigned consecutively (only for JWE2)")
	path: StringProperty(name="Mod Path", description="A folder will be created in this path for the mod files",
						 default="", maxlen=1024, subtype="DIR_PATH")
	pack: StringProperty(name="Pack into",
						 description="Create the ovl files for this mod into this folder, usually one level deep from the ovldata folder",
						 default="", maxlen=1024, subtype="DIR_PATH")


class ModDataPanel(Panel):
	"""Creates a Panel in the Collection properties window for mod attributes"""
	bl_label = "Cobra Mod information"
	bl_idname = "OBJECT_PT_ModDataPanel"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "collection"

	def draw(self, context):
		self.layout.prop(context.collection.mod, "name")
		self.layout.prop(context.collection.mod, "desc")
		self.layout.prop(context.collection.mod, "game")
		self.layout.prop(context.collection.mod, "uuid")
		if context.collection.mod.game == 'JURASSIC_WORLD_EVOLUTION_2':
			self.layout.prop(context.collection.mod, "ordid")
		self.layout.prop(context.collection.mod, "path")
		self.layout.operator("cobra.export_mod")
		self.layout.prop(context.collection.mod, "pack")
		self.layout.operator("cobra.pack_mod")


# endregion

# region Global variables, functions and properties of Object for Mod creation
class SceneryData(PropertyGroup):
	"""Stores enough information to create a mod from this blender file"""
	name: StringProperty(name="Name", description='This is the human-readable name of the asset.')
	desc: StringProperty(name="Description", description="Asset long description.")
	price: FloatProperty(name="Price", min=0)
	cost: FloatProperty(name="Running cost", min=0)


class SceneryDataPanel(Panel):
	"""Creates a Panel in the Object properties window for Scenery asset attributes"""
	bl_label = "Cobra Asset information"
	bl_idname = "OBJECT_PT_SceneryDataPanel"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "object"

	def draw(self, context):
		self.layout.prop(context.object.scenery, "name")
		self.layout.prop(context.object.scenery, "desc")

		row = self.layout.row()
		row.label(text="Gameplay", icon='WORLD_DATA')
		row.prop(context.object.scenery, "price")
		row.prop(context.object.scenery, "cost")

		self.layout.operator("cobra.generate_icon")


# endregion


# region Global variables and properties of Material
class CobraMaterialSettings(VersionedPropertyGroup):
	c = ConstantsProvider(("shaders", "textures"))

	shader_name_pz: EnumProperty(
		name='Shader',
		description='Shader for Planet Zoo',
		items=[(name, name, "") for name in c['Planet Zoo']["textures"]],
	)
	shader_name_jwe2: EnumProperty(
		name='Shader',
		description='Shader for Jurassic World Evolution 2',
		items=[(name, name, "") for name in c['Jurassic World Evolution 2']["textures"]],
	)

	pRenderLayerOverride: IntProperty(name='Render Layer Override', default=-1, min=-1)
	pVerticalTiling: FloatProperty(name='Vertical Tiling', default=0.25, min=0.0)

	pEnableScreenSpaceAO: BoolProperty(name='Enable Screen space Occlussion', default=True)
	pAOTexCoordIndex: IntProperty(name='Occlussion Coord index', default=0, min=0)

	pWeather_Enable: BoolProperty(name='Enable Weather', default=True)
	pEnableWeatherPooling: BoolProperty(name='Enable Weather Pooling', default=True)
	pWeather_ExplicitNormalThreshold: FloatProperty(name='Weather normal threshold', default=0.85, min=0.0)
	pMaximumWaterPermeability: FloatProperty(name='Max water permeability', default=0.5, min=0.0)
	pSnowOnSlopesOffset: FloatProperty(name='Offset snow on slopes', default=0.0, min=0.0)
	pMaximumSnowAmount: FloatProperty(name='Max accumulated snow', default=1.0, min=0.0)

	pEnablePoweredEmissive: BoolProperty(name='Enable Powered Emissive', default=False)
	pEmissiveTint: FloatVectorProperty(
		name="Emissive Tint",
		subtype="COLOR",
		size=4,
		min=0.0,
		max=1.0,
		default=(1.0, 1.0, 1.0, 1.0)
	)
	pEmissiveLightType: IntProperty(name='Emissive Light Type', default=1, min=0)
	pEmissiveLightPower: FloatProperty(name='Emissive Light Power', default=0.5, min=0.0)
	pEmissiveAdaptiveBrighnessWeight: FloatProperty(name='Adaptive Brightness Weight', default=0.0, min=0.0)
	pEmissiveScrollData: FloatVectorProperty(
		name="Emissive Scroll Data",
		subtype='XYZ',
		size=3,
		min=0.0,
		max=1.0,
		default=(0.0, 0.0, 0.0)
	)
	pIsDisplayPanel: BoolProperty(name='Is Display Panel', default=False)

	pEnablePulsingEmissive: BoolProperty(name='Enable Emissive Pulsing', default=True)
	pPulsingEmitFrequency: FloatProperty(name='Emissive Pulsing Frequency', default=1.0, min=0.0)
	pPulsingEmitDarkenScale: FloatProperty(name='Emissive Darken Scale', default=0.8, min=0.0)

	pFlexiColourBlended: BoolProperty(name='Enable Flexicolour', default=True)
	pFlexiColourTexCoordIndex: IntProperty(name='Flexicolour Coord index', default=0, min=0)
	pFlexiColourVertexColour: IntProperty(name='Flexicolour Vertex Colour', default=0, min=0)
	pFlexiColourUseAdditiveBlend: BoolProperty(name='Use Additive Blending', default=False)
	pEnableEmissiveFlexiColour: BoolProperty(name='Enable Emissive Flexicolour', default=False)

	@property
	def shader_name(self):
		return self.get_value(bpy.context, "shader_name")
