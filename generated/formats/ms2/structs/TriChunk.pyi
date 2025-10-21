from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.Vector3 import Vector3
from generated.formats.ms2.structs.AxisAngle import AxisAngle


class TriChunk(BaseStruct):
    bounds: Array[Array[float]]
    bounds_min: Vector3
    material_index: int
    tris_count: int
    bounds_max: Vector3
    tris_index: int
    value_min: int
    tris_offset: int
    zero: int
    loc: Vector3
    rot: AxisAngle
    shell_index: int
    shell_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
