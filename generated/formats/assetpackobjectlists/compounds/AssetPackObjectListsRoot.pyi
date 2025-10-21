from generated.formats.assetpackobjectlists.compounds.AssetPackObjectList import AssetPackObjectList
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class AssetPackObjectListsRoot(MemStruct):
    asset_pack_object_lists_list: ArrayPointer[AssetPackObjectList]
    asset_pack_object_lists_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
