from generated.formats.matcol.compounds.Layer import Layer
from generated.formats.matcol.compounds.Texture import Texture
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class RootFrag(MemStruct):
    mat_type: int
    textures: ArrayPointer[Texture]
    tex_count: int
    materials: ArrayPointer[Layer]
    mat_count: int
    unk: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
