from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.spl.compounds.ByteVector3 import ByteVector3
from generated.formats.spl.compounds.ShortVector3 import ShortVector3


class Key(MemStruct):
    pos: ShortVector3
    handle_left: ByteVector3
    handle_right: ByteVector3
    handle_scale: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
