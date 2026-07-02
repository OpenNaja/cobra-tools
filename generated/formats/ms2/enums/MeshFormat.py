from generated.base_enum import BaseEnum
from generated.formats.base.basic import Ubyte


class MeshFormat(BaseEnum):

	__name__ = 'MeshFormat'
	_storage = Ubyte

	SEPARATE = 0
	SPEEDTREE_32 = 1
	IMPOSTOR_48 = 2
	FOLIAGE_24 = 3
	FOLIAGE_24_NO_BBOX = 5
