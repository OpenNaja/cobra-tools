import enum
import logging
import math
import sys

import bpy
from bpy.props import FloatVectorProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty, StringProperty
from bpy.types import PropertyGroup

from constants import ConstantsProvider
from generated.formats.ms2 import games
from generated.formats.ms2.enums.Jwe1Collision import Jwe1Collision
from generated.formats.ms2.enums.Jwe1Surface import Jwe1Surface
from generated.formats.ms2.enums.PcCollision import PcCollision
from generated.formats.ms2.enums.PcSurface import PcSurface
from generated.formats.ms2.enums.RigidBodyFlag import RigidBodyFlag

from plugin.utils.object import get_view_collections
from plugin.utils.var_names import pz_shader_floats, pz_shader_ints

suffix_map = {
	"Planet Coaster": "_pc",
	"Planet Coaster 2": "_pc2",
	"Jurassic World Evolution": "_jwe",
	"Planet Zoo": "_pz",
	"Jurassic World Evolution 2": "_jwe2",
	"Jurassic World Evolution 3": "_jwe3",
	"Warhammer Age of Sigmar - Realms of Ruin": "_whaos",
}


class VersionedPropertyGroup(PropertyGroup):
	def get_current_game_suffix(self, context):
		game = context.scene.cobra.game
		return suffix_map.get(game, None)

	def get_current_versioned_name(self, context, name):
		game_suffix = self.get_current_game_suffix(context)
		if game_suffix:
			prop_name = f"{name}{game_suffix}"
			if hasattr(self, prop_name):
				return f"{name}{game_suffix}"

	def get_value(self, context, name):
		versioned_prop = self.get_current_versioned_name(context, name)
		if versioned_prop:
			return getattr(self, versioned_prop)
		else:
			logging.warning(f"No game-specific '{name}' property")

	def set_value(self, context, name, v):
		if isinstance(v, enum.Enum):
			v = v.name
		versioned_prop = self.get_current_versioned_name(context, name)
		if versioned_prop:
			setattr(self, versioned_prop, v)
		else:
			logging.warning(f"No game-specific '{name}' property")


def show_lod_callback(self, context):
	logging.debug(f"Showing LOD {self.current_lod}")
	view_colls = get_view_collections()
	for view_coll in view_colls:
		if view_coll.name in context.scene.collection.children:
			# don't alter the visibility of mdl2 collections
			continue
		if "_joints" in view_coll.name:
			# don't alter the visibility of joints collections
			continue
		lod_index = int(math.floor(self.current_lod))
		lod_transition = self.current_lod - lod_index
		view_coll.hide_viewport = f"_L{lod_index}" not in view_coll.name
		# set LOD blending state
		if not view_coll.hide_viewport:
			for ob in view_coll.collection.objects:
				b_keys = ob.data.shape_keys
				if b_keys and "LOD" in b_keys.key_blocks:
					k = b_keys.key_blocks["LOD"]
					k.value = lod_transition


def make_material_callback(var_name):
	def show_material_callback(self, context):
		current_var = getattr(self, var_name)
		current_var_spaced = var_name.replace("_", " ")
		logging.debug(f"Showing Morph {current_var}")
		for mat in bpy.data.materials:
			if mat.use_nodes:
				tree = mat.node_tree
				variation_node = tree.nodes.get("AnimalVariation")
				if variation_node:
					variation_node.inputs[current_var_spaced].default_value = current_var

	return show_material_callback


class LodData(PropertyGroup):
	distance: FloatProperty(min=0.0, precision=0, description="Distance to object for LOD")
	ratio: FloatProperty(min=0.0, max=100.0, precision=1,
						 description="Baseline reduction ratio - final decimation ratio also considers vertex count of L0 geometry")

	def update_values(self, lod_i):
		l_n = [100, 40, 26.666, 15, 8, 3.333]
		self.distance = math.pow(30 + 15 * lod_i, 2)
		self.ratio = l_n[lod_i]


class CobraSceneSettings(PropertyGroup):
	__annotations__ = {}

	game: EnumProperty(
		name='Game',
		description='Cobra game version for this scene',
		items=[(e.value, e.value, "") for e in games],
	)
	num_streams: IntProperty(
		name="External Streams",
		description="Number of lod levels stored in external .modelstream files",
		default=0,
		min=0,
		max=6
	)
	current_lod: FloatProperty(
		name="Current LOD",
		description="LOD index to show",
		default=0.0,
		min=0.0,
		max=5.0,
		update=show_lod_callback
	)
	for f in pz_shader_floats:
		__annotations__[f] = FloatProperty(
			name=f,
			description=f"Sets {f} for all materials",
			default=0.0,
			min=0.0,
			max=1.0,
			update=make_material_callback(f)
		)
	for f in pz_shader_ints:
		__annotations__[f] = IntProperty(
			name=f,
			description=f"Sets {f} for all materials",
			default=-1,
			min=-1,
			max=5,
			update=make_material_callback(f)
		)


class CobraMeshSettings(PropertyGroup):
	pass


class CobraCollisionSettings(VersionedPropertyGroup):
	__annotations__ = {}
	air_resistance: FloatVectorProperty(
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
	damping_3d: FloatVectorProperty(
		name='Damping',
		description='Damping in 3D',
		default=(0.0, 0.0, 0.0),
		min=sys.float_info.min,
		max=sys.float_info.max,
		soft_min=sys.float_info.min,
		soft_max=sys.float_info.max,
		step=1,
		precision=6)
	plasticity_min: FloatProperty(name="Plasticity Lower", subtype="ANGLE")
	plasticity_max: FloatProperty(name="Upper", subtype="ANGLE")
	flag: EnumProperty(
		name='Dynamics Flag',
		description='Current state of this rigidbody',
		items=[(item.name, item.name, "") for i, item in enumerate(RigidBodyFlag)],
	)
	for game, dtype, values in (
			("Planet Coaster", "Surface", [e.name for e in PcSurface]),
			("Planet Coaster", "Surface_2", [e.name for e in PcSurface]),
			("Planet Coaster", "Classification", [e.name for e in PcCollision]),
			("Jurassic World Evolution", "Surface", [e.name for e in Jwe1Surface]),
			("Jurassic World Evolution", "Classification", [e.name for e in Jwe1Collision]),
			("Planet Zoo", "Surface",
			 ['Animal', 'Brick', 'Character', 'Cloth', 'Concrete', 'Default', 'Default_Legacy_DO_NOT_USE', 'Dirt',
			  'Foliage', 'Frictionless', 'Glass', 'Grass', 'Ice', 'Leaves', 'Litter', 'Metal', 'Mud', 'Plastic', 'Poo',
			  'Rubber', 'Sand', 'Snow', 'Stone', 'Tree', 'Trigger', 'Tyre', 'Wood']),
			("Planet Zoo", "Classification",
			 ['Animal', 'Animal_Bone', 'Animal_Box', 'Animal_Dead', 'Animal_Pouncing', 'Balloon', 'Bedding', 'Building',
			  'Character_InFlight', 'Character_Limb', 'Character_Limb_NoCollision', 'Character_Miscreant',
			  'Character_SoS', 'Climbable', 'Coaster', 'Coaster_Car', 'Coaster_Misc', 'Coaster_RacingCar',
			  'DevelopmentOnly_Ball', 'DevelopmentOnly_Character', 'Enrichment_Object', 'Facility', 'Kinetic_Object',
			  'Landscape', 'Navmesh', 'NoCollision', 'Poo', 'Prop', 'Ride', 'Scenery', 'Scenery_NoNavSource',
			  'Scenery_Vandalised', 'Structure', 'Track', 'TrackScenery', 'Track_Support', 'TreeBase', 'TreeBranch',
			  'TreeFoliage', 'TreeTrunk', 'Trigger_AnimalMemorialStaffThoughts', 'Trigger_AnimalObstruction',
			  'Trigger_EducationSource', 'Trigger_EscapedAnimal', 'Trigger_FacilityNegativeInfluence', 'Trigger_Grid',
			  'Trigger_GuestGate', 'Trigger_Inspector', 'Trigger_Presenter', 'Trigger_Queue', 'Trigger_Screen',
			  'Trigger_Security', 'UIElement', 'Water', 'WaterSpray', 'Wheel']),
			("Jurassic World Evolution 2", "Surface",
			 ['BuildingBrick', 'BuildingConcrete', 'BuildingGlass', 'BuildingIce', 'BuildingMetal', 'BuildingSnow',
			  'BuildingWood', 'CarBody', 'CharacterCollidableLimb', 'CharacterFlying', 'CharacterNonCollidableLimb',
			  'Debris', 'Default', 'DinosaurLimb', 'DirtPath', 'Drone', 'Gyrosphere', 'LEGACY_DO_NOT_USE',
			  'LagoonFloor', 'LandscapeDefault', 'LandscapeDirt', 'LandscapeFoliage', 'LandscapeFrictionless',
			  'LandscapeGrass', 'LandscapeIce', 'LandscapeMetal', 'LandscapeMud', 'LandscapePondBottom',
			  'LandscapeSand', 'LandscapeSnow', 'LandscapeStone', 'LandscapeWood', 'LandscapeWoodHollow',
			  'NonCollidableLimb', 'PaleoFoodPoint', 'PropLeaves', 'PropLitter', 'PropMetal', 'PropPlastic',
			  'PropStone', 'PropTree', 'PropWooden', 'SceneryDefault', 'SceneryTree', 'StructureFence', 'StructurePath',
			  'StructurePylon', 'StructureTrack', 'StructureWall', 'Water']),
			("Jurassic World Evolution 2", "Classification",
			 ['AIDrone', 'AIVehicle', 'AIVehicleFindGrid', 'AIVehicleObstacle', 'Audio', 'AviaryTourGate', 'Building',
			  'BuildingAIVehicleObstacle', 'BuildingNoCameraObstacle', 'CameraObstacle', 'CarBody', 'CarObstacle',
			  'Character', 'Debris', 'Default', 'Development', 'DevelopmentAll', 'Dinosaur', 'DinosaurCollisionProxy',
			  'DinosaurDinosaur', 'DinosaurNoBuilding', 'DinosaurNoCollision', 'DinosaurNoFence', 'DinosaurNoVehicle',
			  'DinosaurSelfCollision', 'Drone', 'Fence', 'FlyingVehicleObstacle', 'Foliage', 'Gate', 'Guest',
			  'GuestAvoidance', 'GuestObstacle', 'GuestRagdoll', 'HatcheryGate', 'InvisibleWall', 'LEGACY_DO_NOT_USE',
			  'LagoonFloor', 'Landscape', 'MissionTrigger', 'PaleoFoodPoint', 'Path', 'Perch', 'PerchQuetz', 'Prop',
			  'PropNoCameraObstacle', 'Pylon', 'Rotor', 'TinyDinosaurCollisionProxy', 'TourGate', 'Track', 'Tree',
			  'Vehicle', 'Wall', 'Water', 'WaterSplash', 'Wheel']),
			("Planet Coaster 2", "Surface",
			 ['Ball', 'Brick', 'BuildingMetal', 'BuildingWood', 'Car', 'Character', 'Coaster_DefaultDefault',
			  'Concrete', 'Default', 'Default_DefaultDefault', 'DevelopmentDefault', 'Dirt', 'FacilityDefault',
			  'Foliage', 'Gizmo', 'GizmoPrecise', 'Glass', 'Grass', 'Misc', 'NavMeshDefault', 'Plastic', 'PropMetal',
			  'PropStone', 'RideDefault', 'SceneryPlatformFinder', 'Scenery_DefaultDefault', 'Track_Default', 'Tree',
			  'Water', 'Wooden']),
			("Planet Coaster 2", "Classification",
			 ['Building', 'Coaster', 'Coaster_Car', 'Coaster_Default', 'Default', 'Default_Default', 'Development',
			  'Facility', 'Gizmo', 'GizmoPrecise', 'NavMesh', 'Prop', 'Ride', 'Scenery', 'Scenery_Default',
			  'Scenery_SceneryPlatformFinder', 'Scenery_Tree', 'Track', 'TreeBase', 'TreeFoliage', 'TreeTrunk']),
			("Jurassic World Evolution 3", "Surface",
			 ['BuildingBrick', 'BuildingConcrete', 'BuildingGlass', 'BuildingIce', 'BuildingMetal', 'BuildingSnow',
			  'BuildingWood', 'CarBody', 'CharacterCollidableLimb', 'CharacterFlying', 'CharacterNonCollidableLimb',
			  'Debris', 'Default', 'DinosaurLimb', 'DirtPath', 'Drone', 'Gizmo', 'Gyrosphere', 'LEGACY_DO_NOT_USE',
			  'LagoonFloor', 'LandscapeDefault', 'LandscapeDirt', 'LandscapeFoliage', 'LandscapeFrictionless',
			  'LandscapeGrass', 'LandscapeIce', 'LandscapeMetal', 'LandscapeMud', 'LandscapePath',
			  'LandscapePondBottom', 'LandscapeSand', 'LandscapeSnow', 'LandscapeStone', 'LandscapeWood',
			  'LandscapeWoodHollow', 'NonCollidableLimb', 'PaleoFoodPoint', 'PropLeaves', 'PropLitter', 'PropMetal',
			  'PropMetal_ReducedBounce', 'PropPlastic', 'PropStone', 'PropTree', 'PropWooden', 'SceneryDefault',
			  'SceneryTree', 'StructureFence', 'StructurePath', 'StructurePylon', 'StructureTrack', 'StructureWall',
			  'Water']),
			("Jurassic World Evolution 3", "Classification",
			 ['AIDrone', 'AITourVehicle', 'AIVehicle', 'AIVehicleFindGrid', 'Audio', 'AviaryTourGate', 'Building',
			  'BuildingNoCameraObstacle', 'CameraObstacle', 'CarBody', 'CarObstacle', 'Debris', 'Default',
			  'Development', 'DevelopmentAll', 'Dinosaur', 'DinosaurCollisionProxy', 'DinosaurContainer',
			  'DinosaurDinosaur', 'DinosaurLandscapeOnlyCollision', 'DinosaurNoBuilding', 'DinosaurNoCollision',
			  'DinosaurNoFence', 'DinosaurNoVehicle', 'DinosaurSelfCollision', 'Drone', 'Fence',
			  'FlyingVehicleObstacle', 'Foliage', 'Gate', 'Gizmo', 'Guest', 'GuestAvoidance', 'GuestObstacle',
			  'GuestRagdoll', 'HatcheryGate', 'LEGACY_DO_NOT_USE', 'LagoonFloor', 'Landscape', 'MissionTrigger',
			  'PaleoFoodPoint', 'Path', 'Perch', 'PerchQuetz', 'PhysicsDisabledProp',
			  'PhysicsDisabledPropNoCameraObstacle', 'PhysicsFootplant', 'Prop', 'PropNoCameraObstacle', 'Pylon',
			  'Rotor', 'ScenerySelectionVolume', 'TinyDinosaurCollisionProxy', 'TourGate', 'Track', 'Vehicle',
			  'VehicleReserved', 'VehicleTrigger', 'Wall', 'Water', 'WaterSplash']
			 ),

	):
		identifier = f"{dtype.lower()}{suffix_map.get(game, None)}"
		__annotations__[identifier] = EnumProperty(
			name=dtype,
			description=f"Hitcheck {dtype} Name for {game}",
			items=[(name, name, "") for name in values],
		)


class CobraMaterialSettings(VersionedPropertyGroup):
	c = ConstantsProvider(("shaders", "textures"))

	shader_name_pc: EnumProperty(
		name='Shader',
		description='Shader for Planet Coaster',
		items=[(name, name, "") for name in c['Planet Coaster']["shaders"]],
	)
	shader_name_pc2: EnumProperty(
		name='Shader',
		description='Shader for Planet Coaster 2',
		items=[(name, name, "") for name in c['Planet Coaster 2']["shaders"]],
	)
	shader_name_pz: EnumProperty(
		name='Shader',
		description='Shader for Planet Zoo',
		items=[(name, name, "") for name in c['Planet Zoo']["shaders"]],
	)
	shader_name_jwe: EnumProperty(
		name='Shader',
		description='Shader for Jurassic World Evolution',
		items=[(name, name, "") for name in c['Jurassic World Evolution']["shaders"]],
	)
	shader_name_jwe2: EnumProperty(
		name='Shader',
		description='Shader for Jurassic World Evolution 2',
		items=[(name, name, "") for name in c['Jurassic World Evolution 2']["shaders"]],
	)
	shader_name_jwe3: EnumProperty(
		name='Shader',
		description='Shader for Jurassic World Evolution 3',
		items=[(name, name, "") for name in c['Jurassic World Evolution 3']["shaders"]],
	)
	shader_name_whaos: EnumProperty(
		name='Shader',
		description='Shader for Warhammer Age of Sigmar - Reals of Ruin',
		items=[(name, name, "") for name in c['Warhammer Age of Sigmar - Realms of Ruin']["shaders"]],
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

	@shader_name.setter
	def shader_name(self, v):
		self.set_value(bpy.context, "shader_name", v)


class MATCOL_ListItem(PropertyGroup):
	"""Group of properties representing an item in the list."""
	name: StringProperty(
		name="Name",
		description="A name for this item",
		default="Untitled"
	)
