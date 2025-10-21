from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.terrainindexeddetaillayers.compounds.BrushitemStruct import BrushitemStruct


class TerrainDetailsLayerItem(MemStruct):
    layer_name: Pointer[str]
    info_list: ArrayPointer[BrushitemStruct]
    info_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
