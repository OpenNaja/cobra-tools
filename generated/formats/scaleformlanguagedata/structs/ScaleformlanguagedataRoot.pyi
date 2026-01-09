from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.scaleformlanguagedata.structs.FontInfo import FontInfo
from generated.formats.scaleformlanguagedata.structs.GfxReference import GfxReference


class ScaleformlanguagedataRoot(MemStruct):
    gfx_files: ArrayPointer[GfxReference]
    gfx_files_count: int
    fonts: ArrayPointer[FontInfo]
    fonts_count: int
    zero_2: int
    zero_3: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
