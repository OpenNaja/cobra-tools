from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class LuaModules(MemStruct):
    motion_graph: Pointer[str]
    motion_graph_event_handling: Pointer[str]
    motion_graph_actions: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
