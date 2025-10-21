from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.spl.structs.ByteVector3 import ByteVector3
from generated.formats.spl.structs.ShortVector3 import ShortVector3


class Key(MemStruct):
    pos: ShortVector3
    handle_left: ByteVector3
    handle_right: ByteVector3
    handle_scale: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
