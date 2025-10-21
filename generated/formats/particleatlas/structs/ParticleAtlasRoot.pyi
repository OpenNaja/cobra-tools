from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class ParticleAtlasRoot(MemStruct):
    tex_name: Pointer[str]
    gfr_name: Pointer[str]
    id: int
    zero: int
    dependency_name: Pointer[object]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
