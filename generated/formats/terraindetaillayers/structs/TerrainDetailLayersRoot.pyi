from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.terraindetaillayers.structs.TerrainDetailsLayerItem import TerrainDetailsLayerItem


class TerrainDetailLayersRoot(MemStruct):
    layer_list: ArrayPointer[TerrainDetailsLayerItem]
    layer_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
