from source.formats.base.basic import fmt_member
from generated.formats.base.enum import UintEnum


class FgmDtype(UintEnum):

	"""
	dtypes = {0: "f", 1: "ff", 2: "fff", 3: "ffff", 5: "i", 6: "i"}  # 4:"I", 8:"I"
	"""
	Float = 0
	Float2 = 1
	Float3 = 2
	Float4 = 3
	Int = 5
	Bool = 6
	RGBA = 7
	Texture = 8
