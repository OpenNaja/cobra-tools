from generated.base_struct import BaseStruct
from generated.formats.base.structs.Vector3 import Vector3
from generated.formats.ms2.structs.Matrix33 import Matrix33


class JointTransform(BaseStruct):
    rot: Matrix33
    loc: Vector3

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
