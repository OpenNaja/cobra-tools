from typing import Union
from generated.base_struct import BaseStruct
from generated.formats.ms2.enums.CollisionType import CollisionType
from generated.formats.ms2.enums.Jwe1Collision import Jwe1Collision
from generated.formats.ms2.enums.Jwe1Surface import Jwe1Surface
from generated.formats.ms2.enums.PcCollision import PcCollision
from generated.formats.ms2.enums.PcSurface import PcSurface
from generated.formats.ms2.structs.BoundingBox import BoundingBox
from generated.formats.ms2.structs.Capsule import Capsule
from generated.formats.ms2.structs.ConvexHull import ConvexHull
from generated.formats.ms2.structs.Cylinder import Cylinder
from generated.formats.ms2.structs.MeshCollision import MeshCollision
from generated.formats.ms2.structs.Sphere import Sphere


class HitCheck(BaseStruct):
    dtype: CollisionType
    align: int
    classification_name: PcCollision
    surface_name: PcSurface
    surface_name_2: PcSurface
    classification_name: Jwe1Collision
    surface_name: Jwe1Surface
    classification_name: str
    surface_name: str
    zero_extra_pc: int
    name: str
    collider: Union[BoundingBox, Capsule, ConvexHull, Cylinder, MeshCollision, Sphere]
    zero_extra_zt: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
