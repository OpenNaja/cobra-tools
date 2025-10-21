from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.trackstation.structs.CommonChunk import CommonChunk
from generated.formats.trackstation.structs.ControlBoxInfo import ControlBoxInfo
from generated.formats.trackstation.structs.CornerEdgeTrack import CornerEdgeTrack
from generated.formats.trackstation.structs.FlumeInfo import FlumeInfo
from generated.formats.trackstation.structs.GateInfo import GateInfo


class TrackStationRoot(MemStruct):
    station_grid_sizes: Array[float]
    flags: int
    unknown_ptr: int
    corner_edge_track: Pointer[CornerEdgeTrack]
    track_only: Pointer[CommonChunk]
    control_box_front_panel: Pointer[str]
    control_box_info: Pointer[ControlBoxInfo]
    control_box_left_panel: Pointer[str]
    gate_info: Pointer[GateInfo]
    control_box_right_panel: Pointer[str]
    unknown_56: int
    entrance_gate: Pointer[str]
    flume_info: Pointer[FlumeInfo]
    exit_gate: Pointer[str]
    unknown_72: int
    unk_ints_2: Array[int]
    fence_extrusion: Pointer[str]
    small_fence_extrusion: Pointer[str]
    fence_cap: Pointer[str]
    unk_floats_2: Array[float]
    unk_floats_3: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
