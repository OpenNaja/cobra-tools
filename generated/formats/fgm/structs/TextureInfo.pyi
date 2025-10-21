from typing import Union
from generated.array import Array
from generated.formats.fgm.structs.GenericInfo import GenericInfo
from generated.formats.fgm.structs.TexIndex import TexIndex
from generated.formats.ovl_base.structs.ByteColor import ByteColor


class TextureInfo(GenericInfo):
    value: Union[Array[ByteColor], Array[TexIndex]]
    some_index_0: int
    some_index_1: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
