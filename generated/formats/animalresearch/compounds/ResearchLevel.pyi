from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.ovl_base.compounds.ZStringList import ZStringList


class ResearchLevel(MemStruct):
    level_name: Pointer[str]
    next_levels: Pointer[ZStringList]
    next_levels_count: int
    children: Pointer[ZStringList]
    children_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
