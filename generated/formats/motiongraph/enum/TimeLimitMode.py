from source.formats.base.basic import fmt_member
from generated.formats.base.enum import UintEnum


class TimeLimitMode(UintEnum):
	WRAP = 0
	CLAMP = 1
