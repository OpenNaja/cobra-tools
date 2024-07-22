from generated.base_enum import BaseEnum
from generated.formats.base.basic import Ushort


class PcSurface(BaseEnum):

	__name__ = 'PcSurface'
	_storage = Ushort

	LANDSCAPE = 0
	PROP = 1
	WATER = 2
	CHARACTER = 3
	PROJECTILE = 4
	BUILDING = 5
	TRACK = 6
	CAR_ON_TRACK = 7
	CAR_OFF_TRACK = 8
	VEHICLE = 9
	WHEEL = 10
	NAV_MESH = 11
	U_I_ELEMENT = 12
	RIDE = 13
	TREE = 14
	TRACK_SCENERY = 15
	MISCREANT = 16
	FLAT_RIDE_SCENERY = 17
	DRIVEABLE_CAR = 18
	DRIVE_THRU = 19
