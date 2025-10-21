from generated.formats.assetpackobjectlists.structs.AssetPackObjectList import AssetPackObjectList
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class AssetPackObjectListsRoot(MemStruct):
    asset_pack_object_lists_list: ArrayPointer[AssetPackObjectList]
    asset_pack_object_lists_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
