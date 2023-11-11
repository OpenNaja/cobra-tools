from generated.base_enum import BaseEnum
from generated.formats.base.basic import Uint


class RigidBodyFlag(BaseEnum):

	__name__ = 'RigidBodyFlag'
	_storage = Uint

	STATIC = 0
	DYNAMICS_ASLEEP = 1
	DYNAMICS_AWAKE = 2
