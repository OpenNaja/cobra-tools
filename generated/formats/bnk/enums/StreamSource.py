from generated.base_enum import BaseEnum
from generated.formats.base.basic import Ubyte


class StreamSource(BaseEnum):

	__name__ = 'StreamSource'
	_storage = Ubyte

	EMBEDDED = 0
	STREAMED = 1
	PREFETCHED = 2
