from generated.formats.assetpackobjectlists.structs.SceneryObjectResourceRef import SceneryObjectResourceRef
from generated.formats.assetpackobjectlists.structs.UnitRef import UnitRef
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class AssetPackObjectList(MemStruct):
    asset_pack_object_list_name: Pointer[str]
    scenery_object_resource_items: ArrayPointer[SceneryObjectResourceRef]
    scenery_object_resource_count: int
    unit_items: ArrayPointer[UnitRef]
    unit_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
