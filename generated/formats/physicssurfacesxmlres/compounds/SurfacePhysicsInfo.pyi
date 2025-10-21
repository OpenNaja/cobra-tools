from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.physicssurfacesxmlres.compounds.EmptyStruct import EmptyStruct
from generated.formats.physicssurfacesxmlres.compounds.Surface import Surface


class SurfacePhysicsInfo(MemStruct):
    surface: Surface
    unk_64_1: int
    name_1: Pointer[str]
    name_2: Pointer[str]
    nil: Pointer[EmptyStruct]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
