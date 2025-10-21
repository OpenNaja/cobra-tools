from generated.formats.compoundbrush.structs.BrushIndex import BrushIndex
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class BrushStruct(MemStruct):
    brush_name: Pointer[str]
    index: Pointer[BrushIndex]
    padding: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
