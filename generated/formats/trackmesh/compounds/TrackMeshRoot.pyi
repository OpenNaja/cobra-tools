from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.trackmesh.compounds.Lod import Lod
from generated.formats.trackmesh.compounds.TrackMeshElement import TrackMeshElement
from generated.formats.trackmesh.compounds.TrackMeshObject import TrackMeshObject
from generated.formats.trackmesh.compounds.TrackMeshOffset import TrackMeshOffset


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
