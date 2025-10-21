from generated.formats.habitatboundary.structs.HbPostSize import HbPostSize
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class HbPhysicsOffsets(MemStruct):
    thickness: float
    post_size: HbPostSize
    wall_pad_top: float
    wall_post_gap: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
