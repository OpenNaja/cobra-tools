from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.trackmesh.structs.Lod import Lod
from generated.formats.trackmesh.structs.TrackMeshElement import TrackMeshElement
from generated.formats.trackmesh.structs.TrackMeshObject import TrackMeshObject
from generated.formats.trackmesh.structs.TrackMeshOffset import TrackMeshOffset


class TrackMeshRoot(MemStruct):
    a: int
    offset_data: ArrayPointer[TrackMeshOffset]
    object_data: ArrayPointer[TrackMeshObject]
    element_data: ArrayPointer[TrackMeshElement]
    offset_data_count: int
    object_data_count: int
    element_data_count: int
    lods: ArrayPointer[Lod]
    lods_count: int
    heatmap_name: Pointer[str]
    g: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
