from generated.array import Array
from generated.formats.ms2.compounds.BufferInfo import BufferInfo
from generated.formats.ms2.compounds.BufferPresence import BufferPresence
from generated.formats.ms2.compounds.ModelInfo import ModelInfo
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Ms2Root(MemStruct):
    version: int
    vertex_buffer_count: int
    mdl_2_count: int
    name_count: int
    static_buffer_index: int
    zeros: Array[int]
    buffer_infos: ArrayPointer[BufferInfo]
    model_infos: ArrayPointer[ModelInfo]
    buffer_pointers: ArrayPointer[BufferPresence]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
