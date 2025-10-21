from generated.formats.fgm.compounds.AttribData import AttribData
from generated.formats.fgm.compounds.AttribInfo import AttribInfo
from generated.formats.fgm.compounds.TextureData import TextureData
from generated.formats.fgm.compounds.TextureInfo import TextureInfo
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.ForEachPointer import ForEachPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


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
