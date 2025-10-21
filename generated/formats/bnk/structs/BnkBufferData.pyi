from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.structs.StreamInfo import StreamInfo


class BnkBufferData(BaseStruct):
    size_b: int
    external_aux_b_count: int
    buffer_count: int
    streams_count: int
    zeros: Array[int]
    zeros_per_buffer: Array[Array[int]]
    streams: Array[StreamInfo]
    name: str
    external_b_suffix: str
    external_s_suffix: str

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
