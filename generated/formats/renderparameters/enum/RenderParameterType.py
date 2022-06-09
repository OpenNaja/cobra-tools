from source.formats.base.basic import fmt_member
from generated.formats.base.enum import Uint64Enum


class RenderParameterType(Uint64Enum):
	Bool = 0
	Float = 1
	Int = 2
	UInt = 3
	Float2 = 4
	Float3 = 5
	Float4 = 6
	Colour = 7
	ColourHDR = 8
	String = 9
