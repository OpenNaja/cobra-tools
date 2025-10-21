from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class WorldSharedSettingsHeader(MemStruct):
    biome_name: Pointer[str]
    world_type: int
    skirt_package_name: Pointer[str]
    unknown: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
