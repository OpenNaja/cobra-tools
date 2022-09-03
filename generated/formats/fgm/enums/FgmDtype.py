from generated.base_enum import BaseEnum
from generated.formats.base.basic import Uint


class FgmDtype(BaseEnum):

	__name__ = 'FgmDtype'
	_storage = Uint

	FLOAT = 0
	FLOAT_2 = 1
	FLOAT_3 = 2
	FLOAT_4 = 3
	INT = 5
	BOOL = 6
	RGBA = 7
	TEXTURE = 8
