from generated.formats.achievements.structs.Achievement import Achievement
from generated.formats.achievements.structs.ConditionCheck import ConditionCheck
from generated.formats.achievements.structs.ConditionVarPtr import ConditionVarPtr
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class AchievementsRoot(MemStruct):
    condition_vars: ArrayPointer[ConditionVarPtr]
    condition_vars_count: int
    condition_checks: ArrayPointer[ConditionCheck]
    condition_checks_count: int
    c: ArrayPointer[Achievement]
    c_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
