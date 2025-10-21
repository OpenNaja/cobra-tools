from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.spatialuitheme.compounds.SpatialUIThemeTexture import SpatialUIThemeTexture


class SpatialUIThemeRoot(MemStruct):
    spatial_u_i_theme_texture_list: ArrayPointer[SpatialUIThemeTexture]
    spatial_u_i_theme_texture_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
