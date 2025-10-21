from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.compounds.Vector3 import Vector3
from generated.formats.ms2.compounds.Matrix33 import Matrix33


class BoundingBox(BaseStruct):
    rotation: Matrix33
    center: Vector3
    extent: Vector3
    zeros: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
