from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.path.compounds.PathMaterialData import PathMaterialData


class PathMaterial(MemStruct):
    elevated_mat: Pointer[str]
    elevated_mat_valid: Pointer[str]
    elevated_mat_invalid: Pointer[str]
    terrain_mat: Pointer[str]
    terrain_mat_valid: Pointer[str]
    terrain_mat_invalid: Pointer[str]
    underside_mat_1: Pointer[str]
    underside_mat_2: Pointer[str]
    stairs_mat_1: Pointer[str]
    stairs_mat_2: Pointer[str]
    path_sub_type: int
    mat_data: ArrayPointer[PathMaterialData]
    num_data: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
