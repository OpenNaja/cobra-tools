from generated.formats.base.enums import Uint64Enum


class RenderParameterType(Uint64Enum):

	__name__ = RenderParameterType
	BOOL = 0
	FLOAT = 1
	INT = 2
	U_INT = 3
	FLOAT_2 = 4
	FLOAT_3 = 5
	FLOAT_4 = 6
	COLOUR = 7
	COLOUR_H_D_R = 8
	STRING = 9
