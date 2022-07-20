from source.formats.base.basic import fmt_member
from generated.formats.base.enum import UintEnum


class FgmDtype(UintEnum):

	"""
	dtypes = {0: "f", 1: "ff", 2: "fff", 3: "ffff", 5: "i", 6: "i"}  # 4:"I", 8:"I"
	"""
	FLOAT = 0
	FLOAT_2 = 1
	FLOAT_3 = 2
	FLOAT_4 = 3
	INT = 5
	BOOL = 6
	RGBA = 7
	TEXTURE = 8
