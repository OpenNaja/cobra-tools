from generated.base_struct import BaseStruct
from generated.formats.base.structs.PadAlign import PadAlign
from generated.formats.ovl_base.structs.Empty import Empty


class String32(BaseStruct):
    ref: Empty
    name: str
    pad: PadAlign[object]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
