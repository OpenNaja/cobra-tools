from generated.formats.casinolod.structs.LodGroup import LodGroup
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class CasinoLodRoot(MemStruct):
    lod_name: Pointer[str]
    lod_groups: ArrayPointer[LodGroup]
    lod_groups_count: int
    zero: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
