from generated.base_struct import BaseStruct
from generated.formats.base.compounds.Vector3 import Vector3
from generated.formats.base.compounds.Vector4 import Vector4


class Bone(BaseStruct):
    loc: Vector3
    scale: float
    rot: Vector4
    loc: Vector3
    scale: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
