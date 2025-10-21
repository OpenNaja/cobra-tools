from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class BaniRoot(MemStruct):
    banis: Pointer[object]
    index: int
    offset: int
    read_start_frame: int
    num_frames: int
    animation_length: float
    loop_flag: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
