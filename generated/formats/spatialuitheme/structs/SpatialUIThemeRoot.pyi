from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.spatialuitheme.structs.SpatialUIThemeTexture import SpatialUIThemeTexture


class SpatialUIThemeRoot(MemStruct):
    spatial_u_i_theme_texture_list: ArrayPointer[SpatialUIThemeTexture]
    spatial_u_i_theme_texture_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
