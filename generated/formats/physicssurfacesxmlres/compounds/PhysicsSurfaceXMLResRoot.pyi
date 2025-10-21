from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.physicssurfacesxmlres.compounds.ArrWrapper import ArrWrapper
from generated.formats.physicssurfacesxmlres.compounds.EmptyStruct import EmptyStruct
from generated.formats.physicssurfacesxmlres.compounds.OnlyName import OnlyName
from generated.formats.physicssurfacesxmlres.compounds.Struct2 import Struct2
from generated.formats.physicssurfacesxmlres.compounds.Surface import Surface
from generated.formats.physicssurfacesxmlres.compounds.SurfacePhysicsInfo import SurfacePhysicsInfo


class PhysicsSurfaceXMLResRoot(MemStruct):
    default_surface: Surface
    unk_64_1: int
    name_1: Pointer[str]
    name_2: Pointer[str]
    nil_ptr: Pointer[EmptyStruct]
    only_names_j_w_e_1: ArrWrapper[OnlyName]
    surfaces: ArrWrapper[SurfacePhysicsInfo]
    arr_2: ArrWrapper[Struct2]
    only_names: ArrWrapper[OnlyName]
    unk_32_2: int
    unk_32_3: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
