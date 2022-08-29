from generated.base_enum import BaseEnum
from generated.formats.base.basic import Uint


class TimeLimitMode(BaseEnum):

	__name__ = 'TimeLimitMode'
	_storage = Uint

	WRAP = 0
	CLAMP = 1
