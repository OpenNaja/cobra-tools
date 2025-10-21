from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.ovl_base.compounds.ZStringList import ZStringList


class NavigationModeFilter(MemStruct):
    navigation_mode_filter_name: Pointer[str]
    navigation_mode_filter_flags: Pointer[ZStringList]
    navigation_mode_filter_flags_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
