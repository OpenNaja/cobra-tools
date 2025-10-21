from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.physicssurfacesxmlres.compounds.EmptyStruct import EmptyStruct
from generated.formats.physicssurfacesxmlres.compounds.Surface import Surface


class Struct2Sub(MemStruct):
    surface: Surface
    c: int
    d: int
    e: int
    f: int
    nil: Pointer[EmptyStruct]
    bitflag: int
    unkflag: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
