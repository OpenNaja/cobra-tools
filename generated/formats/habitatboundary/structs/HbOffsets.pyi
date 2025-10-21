from generated.formats.habitatboundary.structs.HbPhysicsOffsets import HbPhysicsOffsets
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class HbOffsets(MemStruct):
    physics: HbPhysicsOffsets
    post_height_offset: float
    wall_height: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
