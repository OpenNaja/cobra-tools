from source.formats.base.basic import fmt_member
from generated.formats.base.enum import UintEnum


class TimeLimitMode(UintEnum):
	Wrap = 0
	Clamp = 1
