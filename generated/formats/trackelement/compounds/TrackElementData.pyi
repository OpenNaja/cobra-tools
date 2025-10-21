from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.trackelement.compounds.TrackMeshRef import TrackMeshRef


class TrackElementData(MemStruct):
    spline_name: Pointer[str]
    u_1: Pointer[str]
    u_2: Pointer[str]
    trackmesh_element_name: Pointer[str]
    trackmeshlist: ArrayPointer[TrackMeshRef]
    trackmeshlist_count: int
    unk_count: int
    optional_catwalk: Pointer[str]
    direction: int
    unk_2: int
    unk_3: int
    unk_4: int
    unk_5: int
    unk_6: int
    unk_7: int
    offset: float
    unk_9: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
