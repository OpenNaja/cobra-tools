from generated.formats.ovl_base.structs.MemStruct import MemStruct


class HbPropPhysics(MemStruct):
    pad_top: float
    z_pos: float
    half_width: float
    pad_bottom: float
    half_depth: float
    u_6: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
