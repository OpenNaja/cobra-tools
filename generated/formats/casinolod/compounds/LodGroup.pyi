from generated.formats.casinolod.compounds.Lod import Lod
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class LodGroup(MemStruct):
    lod_name: Pointer[str]
    lods: ArrayPointer[Lod]
    lods_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
