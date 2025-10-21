from generated.formats.biome.structs.BiomeArtIcon import BiomeArtIcon
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.ovl_base.structs.ZStringList import ZStringList


class BiomeArtSettingsRoot(MemStruct):
    packages_to_load: Pointer[ZStringList]
    packages_to_load_count: int
    default_full_scale_material_name: Pointer[str]
    material_names: Pointer[ZStringList]
    material_names_count: int
    brush_name: Pointer[str]
    brush_package: Pointer[str]
    material_icons: ArrayPointer[BiomeArtIcon]
    material_icons_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
