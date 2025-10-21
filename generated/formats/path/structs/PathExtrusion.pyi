from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class PathExtrusion(MemStruct):
    model: Pointer[str]
    post_model: Pointer[str]
    endcap_model: Pointer[str]
    unk_float_1: float
    unk_float_2: float
    is_kerb: bool
    is_not_ground: bool
    post_count: int
    has_posts: bool

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
