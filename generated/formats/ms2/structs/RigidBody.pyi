from generated.base_struct import BaseStruct
from generated.formats.base.structs.Vector3 import Vector3
from generated.formats.ms2.enums.RigidBodyFlag import RigidBodyFlag


class RigidBody(BaseStruct):
    flag: RigidBodyFlag
    loc: Vector3
    mass: float
    air_resistance_x: float
    unk_1: float
    unk_2: float
    air_resistance_y: float
    unk_4: float
    air_resistance_z: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
