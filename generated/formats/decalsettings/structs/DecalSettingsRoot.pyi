from generated.formats.decalsettings.structs.DecalSettingItem import DecalSettingItem
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class DecalSettingsRoot(MemStruct):
    atlas_name: Pointer[str]
    layer_list: ArrayPointer[DecalSettingItem]
    layer_count: int
    unknown: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
