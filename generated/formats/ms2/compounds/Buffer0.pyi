from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.compounds.PadAlign import PadAlign
from generated.formats.ms2.compounds.StreamsZTHeader import StreamsZTHeader


class Buffer0(BaseStruct):
    name_hashes: Array[int]
    names: Array[str]
    names_padding: PadAlign[object]
    zt_streams_header: StreamsZTHeader

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
