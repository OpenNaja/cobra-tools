from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.ovl_base.compounds.ZStringList import ZStringList
from generated.formats.terraindetaillayers.compounds.DetailStruct import DetailStruct
from generated.formats.terraindetaillayers.compounds.InfoStruct import InfoStruct


class TerrainDetailsLayerItem(MemStruct):
    layer_name: Pointer[str]
    info_list: ArrayPointer[InfoStruct]
    info_count: int
    float_1: float
    float_2: float
    float_3: float
    float_4: float
    float_5: float
    float_6: float
    unk_2: int
    detail_list: ArrayPointer[DetailStruct]
    detail_count: int
    floata_1: float
    floata_2: float
    floata_3: float
    floata_4: float
    floata_5: float
    floata_6: float
    floata_7: float
    floata_8: float
    unk_3_flags: int
    unk_count: int
    other_names: Pointer[ZStringList]
    other_names_count: int
    second_name: Pointer[str]
    floatb_1: float
    floatb_2: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
