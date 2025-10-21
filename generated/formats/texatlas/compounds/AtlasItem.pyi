from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class AtlasItem(MemStruct):
    atlas_name: Pointer[str]
    startx: float
    starty: float
    endx: float
    endy: float
    layer: int
    flags_1: int
    flags_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
