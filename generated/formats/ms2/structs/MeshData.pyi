import numpy as np
from generated.formats.ms2.structs.BufferInfo import BufferInfo
from generated.formats.ovl_base.structs.LookupPointer import LookupPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class MeshData(MemStruct):
    dt: np.dtype
    stream_index: int
    stream_info: LookupPointer[BufferInfo]
    some_index: int
    some_index_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
