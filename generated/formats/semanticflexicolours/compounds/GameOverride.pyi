from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.ovl_base.compounds.ZStringList import ZStringList


class GameOverride(MemStruct):
    game_names: Pointer[ZStringList]
    game_names_count: int
    flexi_names: Pointer[ZStringList]
    num_flexi_names: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
