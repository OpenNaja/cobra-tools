from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.trackstation.compounds.FrontMidBack import FrontMidBack


class CommonChunk(MemStruct):
    width: float
    height: float
    top: FrontMidBack
    base: FrontMidBack
    supports: FrontMidBack

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
