from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.trackelement.bitfields.TracktypeBitfield import TracktypeBitfield
from generated.formats.trackelement.structs.TrackMeshRef import TrackMeshRef


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
    tracktype_bitfield: TracktypeBitfield
    start_connection_bitfield: int
    end_connection_bitfield: int
    offset: float
    unk_5: int
    x_offset: float
    y_offset: float
    z_offset: float
    yaw_offset: float
    pitch_offset: float
    roll_offset: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
