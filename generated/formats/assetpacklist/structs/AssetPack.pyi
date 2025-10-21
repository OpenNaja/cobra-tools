from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class AssetPack(MemStruct):
    asset_pack_name: Pointer[str]
    asset_pack_ui_name: Pointer[str]
    asset_pack_ui_description: Pointer[str]
    asset_pack_asset_package: Pointer[str]
    asset_pack_list_flags_1: int
    asset_pack_list_flags_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
