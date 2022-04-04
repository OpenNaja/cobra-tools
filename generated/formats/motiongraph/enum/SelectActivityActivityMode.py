from source.formats.base.basic import fmt_member
from generated.formats.base.enum import UintEnum


class SelectActivityActivityMode(UintEnum):
	AdvanceChildrenTogether = 0
	RestartChildrenOnSelection = 1
	ChooseOnceAtStart = 2
