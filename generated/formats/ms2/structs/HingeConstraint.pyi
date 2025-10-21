from generated.formats.base.structs.Vector3 import Vector3
from generated.formats.ms2.structs.Constraint import Constraint
from generated.formats.ms2.structs.RotationRange import RotationRange


class HingeConstraint(Constraint):
    direction: Vector3
    limits: RotationRange

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
