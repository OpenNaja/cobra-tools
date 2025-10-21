from generated.base_struct import BaseStruct
from generated.formats.voxelskirt.compounds.Vector3F import Vector3F


class EntityInstance(BaseStruct):
    loc: Vector3F
    z_rot: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
