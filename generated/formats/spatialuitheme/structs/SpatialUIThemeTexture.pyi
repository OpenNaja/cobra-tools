from generated.formats.ovl_base.structs.ByteColor import ByteColor
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class SpatialUIThemeTexture(MemStruct):
    spatial_u_i_theme_texture_id: int
    spatial_u_i_theme_texture_name: Pointer[str]
    spatial_u_i_theme_colour: ByteColor
    spatial_u_i_theme_colour_unknown: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
