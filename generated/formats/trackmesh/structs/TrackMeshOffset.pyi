from generated.formats.base.structs.Vector3 import Vector3
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class TrackMeshOffset(MemStruct):
    offset_id: Pointer[str]
    mdl_2_name: Pointer[str]
    bone_name: Pointer[str]
    relative_offset: Vector3
    spacing: float
    one: int
    min_pitch: float
    min_yaw: float
    flags: int
    z_4: int
    z_5: int
    z_6: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
