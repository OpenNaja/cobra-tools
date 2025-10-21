from generated.formats.base.compounds.Vector3 import Vector3
from generated.formats.ms2.compounds.Constraint import Constraint
from generated.formats.ms2.compounds.Matrix33 import Matrix33
from generated.formats.ms2.compounds.RotationRange import RotationRange


class RagdollConstraint(Constraint):
    vec_a: Vector3
    rot: Matrix33
    vec_b: Vector3
    x: RotationRange
    y: RotationRange
    z: RotationRange
    plasticity: RotationRange

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
