from generated.formats.frenderlodspec.structs.LODGroup import LODGroup
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class FRenderLodSpecRoot(MemStruct):
    lod_groups: ArrayPointer[LODGroup]
    lod_groups_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
