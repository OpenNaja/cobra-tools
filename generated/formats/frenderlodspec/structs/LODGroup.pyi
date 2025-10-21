from generated.formats.frenderlodspec.structs.LODPoints import LODPoints
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class LODGroup(MemStruct):
    group_name: Pointer[str]
    unk_float_1: float
    max_model_bounding_sphere_radius: float
    lod_points: LODPoints
    sub_lod_points_count: int
    sub_lod_points: ArrayPointer[LODPoints]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
