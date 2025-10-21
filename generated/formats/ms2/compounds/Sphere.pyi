from generated.base_struct import BaseStruct
from generated.formats.base.compounds.Vector3 import Vector3


class Sphere(BaseStruct):
    center: Vector3
    radius: float
    zero: int
    zeros_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
