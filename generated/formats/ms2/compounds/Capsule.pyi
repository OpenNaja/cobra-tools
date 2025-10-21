from generated.base_struct import BaseStruct
from generated.formats.base.compounds.Vector3 import Vector3


class Capsule(BaseStruct):
    offset: Vector3
    direction: Vector3
    radius: float
    extent: float
    zero: int
    zeros_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
