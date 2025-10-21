from generated.formats.achievements.compounds.ConditionVar import ConditionVar
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ConditionRef(MemStruct):
    mode: int
    condition_var: Pointer[ConditionVar]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
