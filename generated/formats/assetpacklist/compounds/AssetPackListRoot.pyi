from generated.formats.assetpacklist.compounds.AssetPack import AssetPack
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class AssetPackListRoot(MemStruct):
    asset_pack_list_version: int
    asset_pack_list_list: ArrayPointer[AssetPack]
    asset_pack_list_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
