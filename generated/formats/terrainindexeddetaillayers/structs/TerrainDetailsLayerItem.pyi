from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.terrainindexeddetaillayers.structs.BrushitemStruct import BrushitemStruct


class TerrainDetailsLayerItem(MemStruct):
    layer_name: Pointer[str]
    info_list: ArrayPointer[BrushitemStruct]
    info_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
