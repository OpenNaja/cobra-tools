from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.PadAlign import PadAlign
from generated.formats.base.structs.Vector3 import Vector3
from generated.formats.manis.structs.FloatsGrabber import FloatsGrabber
from generated.formats.manis.structs.Segment import Segment
from generated.formats.manis.structs.SegmentsReader import SegmentsReader
from generated.formats.manis.structs.String32 import String32
from generated.formats.ovl_base.structs.Empty import Empty


class CompressedManiData(BaseStruct):
    frame_count: int
    ori_bone_count: int
    pos_bone_count: int
    scl_bone_count: int
    morph_bone_count: int
    zeros_18: Array[int]
    name_a: String32
    scale_min: Vector3
    scale_max: Vector3
    ptr_first_segment: int
    unk_1: int
    unk_2: int
    segment_count: int
    quantisation_level: int
    unk_1: int
    unk_2: int
    ref_2: Empty
    unk_3: int
    loc_bound_indices: Array[int]
    anoth_pad: PadAlign[object]
    loc_bounds: FloatsGrabber
    anoth_pad_2: PadAlign[object]
    segments: Array[Segment]
    segments_data: SegmentsReader

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
