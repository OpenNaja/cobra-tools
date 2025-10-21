from generated.formats.habitatboundary.structs.HbDoorCutout import HbDoorCutout
from generated.formats.habitatboundary.structs.HbPostPos import HbPostPos
from generated.formats.habitatboundary.structs.HbPropPhysics import HbPropPhysics
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class HabitatBoundaryPropRoot(MemStruct):
    type: int
    prefab: Pointer[str]
    u_1: int
    post: Pointer[str]
    wall: Pointer[str]
    is_guest: int
    post_position: HbPostPos
    u_2: float
    door_physics: HbPropPhysics
    path_physics: HbPropPhysics
    path_join_part: Pointer[str]
    door_cutout: HbDoorCutout
    small: int
    height: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
