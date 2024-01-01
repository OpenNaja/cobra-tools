from generated.base_enum import BaseEnum
from generated.formats.base.basic import Ubyte


class ActionScope(BaseEnum):

	__name__ = 'ActionScope'
	_storage = Ubyte

	GAME_OBJECT_SWITCH = 1
	GLOBAL = 2
	GAME_OBJECT_ID = 3
	GAME_OBJECT_STATE = 4
	ALL = 5
	ALL_EXCEPT_ID = 9
