from generated.array import Array
from generated.formats.base.structs.Vector3 import Vector3
from generated.formats.ms2.bitfields.RenderFlag import RenderFlag
from generated.formats.ms2.structs.LodInfo import LodInfo
from generated.formats.ms2.structs.MaterialName import MaterialName
from generated.formats.ms2.structs.MeshDataWrap import MeshDataWrap
from generated.formats.ms2.structs.Object import Object
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class ModelInfo(MemStruct):
    unk_dla: int
    bounds_min: Vector3
    precision: float
    bounds_max: Vector3
    pack_base: float
    center: Vector3
    radius: float
    num_lods_2: int
    zero: int
    bounds_min_repeat: Vector3
    bounds_max_repeat: Vector3
    num_materials: int
    num_lods: int
    num_objects: int
    num_meshes: int
    last_count: int
    render_flag: RenderFlag
    unks: Array[int]
    pad: Array[int]
    materials: ArrayPointer[MaterialName]
    lods: ArrayPointer[LodInfo]
    objects: ArrayPointer[Object]
    meshes: ArrayPointer[MeshDataWrap]
    first_model: Pointer[object]
    zeros: Array[int]
    increment_flag: int
    zero_0: int
    zero_1: int
    zero_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
