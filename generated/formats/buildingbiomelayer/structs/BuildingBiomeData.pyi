from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class BuildingBiomeData(MemStruct):
    layer: int
    name_1: Pointer[str]
    name_2: Pointer[str]
    padding: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
