from generated.formats.base.structs.Vector3 import Vector3
from generated.formats.ms2.structs.Constraint import Constraint
from generated.formats.ms2.structs.Matrix33 import Matrix33
from generated.formats.ms2.structs.RotationRange import RotationRange


class RagdollConstraint(Constraint):
    vec_a: Vector3
    rot: Matrix33
    vec_b: Vector3
    x: RotationRange
    y: RotationRange
    z: RotationRange
    plasticity: RotationRange

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
