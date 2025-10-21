from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.Vector3 import Vector3
from generated.formats.ms2.structs.Matrix33 import Matrix33


class ConvexHull(BaseStruct):
    vertex_count: int
    rotation: Matrix33
    offset: Vector3
    zeros: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
