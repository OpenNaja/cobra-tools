from source.formats.base.basic import fmt_member
from generated.formats.base.enum import UintEnum


class Compression(UintEnum):
	NONE = 0
	ZLIB = 1
	OODLE = 4
