from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.texatlas.structs.AtlasItem import AtlasItem
from generated.formats.texatlas.structs.TextureData import TextureData


class TexAtlasRoot(MemStruct):
    texture_list: ArrayPointer[TextureData]
    texture_count: int
    atlas_list: ArrayPointer[AtlasItem]
    atlas_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
