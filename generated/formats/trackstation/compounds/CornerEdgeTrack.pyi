from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.trackstation.compounds.CommonChunk import CommonChunk


class CornerEdgeTrack(MemStruct):
    corner: CommonChunk
    edge: CommonChunk
    track: CommonChunk
    zero: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
