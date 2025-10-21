from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.terraindetaillayers.structs.BrushitemStruct import BrushitemStruct


class InfoStruct(MemStruct):
    brush_list: ArrayPointer[BrushitemStruct]
    brush_count: int
    brush_flags: int
    scale: float
    unk_1: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
