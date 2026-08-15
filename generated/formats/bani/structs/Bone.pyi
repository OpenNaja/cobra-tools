from generated.base_struct import BaseStruct
from generated.formats.bani.structs.Vector3Ushort import Vector3Ushort


class Bone(BaseStruct):
    rot: Vector3Ushort
    loc: Vector3Ushort

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
