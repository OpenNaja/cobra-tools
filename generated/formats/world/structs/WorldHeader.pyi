from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.ovl_base.structs.ZStringList import ZStringList


class WorldHeader(MemStruct):
    world_type: int
    asset_pkgs: Pointer[ZStringList]
    asset_pkgs_count: int
    lua_name: Pointer[str]
    ptr_0: Pointer[object]
    ptr_1: Pointer[object]
    prefabs: Pointer[ZStringList]
    ptr_2: Pointer[object]
    prefabs_count: int
    ptr_3: Pointer[object]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
