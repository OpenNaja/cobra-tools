from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class PathResource(MemStruct):
    pathtype: Pointer[str]
    pathmaterial: Pointer[str]
    pathextrusion_kerb: Pointer[str]
    pathextrusion_railing: Pointer[str]
    pathextrusion_ground: Pointer[str]
    pathsupport: Pointer[str]
    path_type: int
    path_sub_type: int
    unk_byte_1: int
    unk_byte_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
