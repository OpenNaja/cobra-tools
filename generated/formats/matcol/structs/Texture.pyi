from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class Texture(MemStruct):
    fgm_name: Pointer[str]
    texture_suffix: Pointer[str]
    texture_type: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
