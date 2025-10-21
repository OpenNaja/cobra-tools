from generated.formats.casinolod.compounds.LodGroup import LodGroup
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class CasinoLodRoot(MemStruct):
    lod_name: Pointer[str]
    lod_groups: ArrayPointer[LodGroup]
    lod_groups_count: int
    zero: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
