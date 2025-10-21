from generated.formats.fgm.structs.AttribData import AttribData
from generated.formats.fgm.structs.AttribInfo import AttribInfo
from generated.formats.fgm.structs.TextureData import TextureData
from generated.formats.fgm.structs.TextureInfo import TextureInfo
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.ForEachPointer import ForEachPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class FgmHeader(MemStruct):
    textures_count: int
    attributes_count: int
    textures: ArrayPointer[TextureInfo]
    attributes: ArrayPointer[AttribInfo]
    name_foreach_textures: ForEachPointer[TextureData]
    value_foreach_attributes: ForEachPointer[AttribData]
    unk_0: int
    unk_1: int
    unk_2: int
    unk_3: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
