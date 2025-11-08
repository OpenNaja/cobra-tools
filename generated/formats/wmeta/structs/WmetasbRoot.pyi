from typing import Union
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.wmeta.structs.BnkMeta import BnkMeta
from generated.formats.wmeta.structs.BnkMetaNew import BnkMetaNew


class WmetasbRoot(MemStruct):
    bnks: Union[ArrayPointer[BnkMetaNew], ArrayPointer[BnkMeta]]
    bnks_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
