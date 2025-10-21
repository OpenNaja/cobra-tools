from generated.formats.buildingbiomelayer.compounds.BuildingBiomeData import BuildingBiomeData
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class BuildingBiomeLayerRoot(MemStruct):
    set_id_name: Pointer[str]
    layer_data: ArrayPointer[BuildingBiomeData]
    count: int
    unk_2_found_as_0: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
