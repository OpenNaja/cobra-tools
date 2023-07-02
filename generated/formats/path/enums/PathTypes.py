from generated.base_enum import BaseEnum
from generated.formats.base.basic import Ubyte


class PathTypes(BaseEnum):

	"""
	taken from PZ c0paths.fdb
	"""

	__name__ = 'PathTypes'
	_storage = Ubyte

	STANDARD = 0
	QUEUE = 1
	STAFF = 2
