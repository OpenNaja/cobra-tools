from typing import Union
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.wmeta.structs.Jwe2WmetasbMain import Jwe2WmetasbMain
from generated.formats.wmeta.structs.WmetasbMain import WmetasbMain


class WmetasbRoot(MemStruct):
    levels: Union[ArrayPointer[Jwe2WmetasbMain], ArrayPointer[WmetasbMain]]
    count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
