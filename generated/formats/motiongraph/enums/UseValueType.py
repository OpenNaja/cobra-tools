from generated.base_enum import BaseEnum
from generated.formats.base.basic import Ushort


class UseValueType(BaseEnum):

	__name__ = 'UseValueType'
	_storage = Ushort

	PROPERTY = 0
	OVERRIDE = 1
	DETECT = 2
