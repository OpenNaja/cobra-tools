from generated.base_enum import BaseEnum
from generated.formats.base.basic import Uint64


class PcCollision(BaseEnum):

	__name__ = 'PcCollision'
	_storage = Uint64

	DEFAULT = 0
	LANDSCAPE = 1
	PROP = 2
	WATER = 4
	CHARACTER = 8
	PROJECTILE = 16
	BUILDING = 32
	TRACK = 64
	CAR_ON_TRACK = 128
	CAR_OFF_TRACK = 256
	VEHICLE = 512
	WHEEL = 1024
	NAV_MESH = 2048
	U_I_ELEMENT = 4096
	RIDE = 8192
	TREE = 16384
	TRACK_SCENERY = 32768
	MISCREANT = 65536
	FLAT_RIDE_SCENERY = 131072
	DRIVEABLE_CAR = 262144
	DRIVE_THRU = 524288
