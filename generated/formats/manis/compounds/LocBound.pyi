from generated.base_struct import BaseStruct
from generated.formats.base.compounds.Vector3 import Vector3


class LocBound(BaseStruct):
    loc_min: Vector3
    loc_extent: Vector3

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
