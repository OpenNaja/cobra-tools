from generated.formats.achievements.structs.ConditionVar import ConditionVar
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class ConditionVarPtr(MemStruct):
    condition_var: Pointer[ConditionVar]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
