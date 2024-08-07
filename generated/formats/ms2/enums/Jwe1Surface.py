from generated.base_enum import BaseEnum
from generated.formats.base.basic import Uint


class Jwe1Surface(BaseEnum):

	__name__ = 'JWE1Surface'
	_storage = Uint

	LEGACY_DO_NOT_USE = 0
	DEFAULT = 1
	LANDSCAPE_DEFAULT = 2
	LANDSCAPE_FRICTIONLESS = 3
	LANDSCAPE_DIRT = 4
	LANDSCAPE_GRASS = 5
	LANDSCAPE_ICE = 6
	LANDSCAPE_METAL = 7
	LANDSCAPE_MUD = 8
	LANDSCAPE_POND_BOTTOM = 9
	LANDSCAPE_SAND = 10
	LANDSCAPE_SNOW = 11
	LANDSCAPE_STONE = 12
	LANDSCAPE_WOOD = 13
	LANDSCAPE_WOOD_HOLLOW = 14
	LANDSCAPE_FOLIAGE = 15
	WATER = 16
	BUILDING_BRICK = 17
	BUILDING_CONCRETE = 18
	BUILDING_GLASS = 19
	BUILDING_ICE = 20
	BUILDING_METAL = 21
	BUILDING_SNOW = 22
	BUILDING_WOOD = 23
	PROP_TREE = 24
	PROP_LEAVES = 25
	PROP_METAL = 26
	PROP_WOODEN = 27
	PROP_PLASTIC = 28
	PROP_STONE = 29
	PROP_LITTER = 30
	DIRT_PATH = 31
	CHARACTER_COLLIDABLE_LIMB = 32
	CHARACTER_NON_COLLIDABLE_LIMB = 33
	CHARACTER_FLYING = 34
	NON_COLLIDABLE_LIMB = 35
	SCENERY_DEFAULT = 36
	SCENERY_TREE = 37
	STRUCTURE_WALL = 38
	STRUCTURE_FENCE = 39
	STRUCTURE_PYLON = 40
	STRUCTURE_PATH = 41
	STRUCTURE_TRACK = 42
	GYROSPHERE = 43
	CAR_BODY = 44
	DEBRIS = 45
	DINOSAUR_LIMB = 46
