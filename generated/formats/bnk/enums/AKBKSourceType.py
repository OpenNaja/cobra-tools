from generated.base_enum import BaseEnum
from generated.formats.base.basic import Ubyte


class AKBKSourceType(BaseEnum):

	__name__ = 'AKBKSourceType'
	_storage = Ubyte

	DATA = 0
	PREFETCH_STREAMING = 1
	STREAMING = 2
