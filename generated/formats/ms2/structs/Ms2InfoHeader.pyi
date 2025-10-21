from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.ms2.structs.Buffer0 import Buffer0
from generated.formats.ms2.structs.BufferInfo import BufferInfo
from generated.formats.ms2.structs.BufferPresence import BufferPresence
from generated.formats.ms2.structs.ModelInfo import ModelInfo
from generated.formats.ms2.structs.ModelReader import ModelReader
from generated.formats.ms2.structs.Ms2Root import Ms2Root


class Ms2InfoHeader(BaseStruct):
    biosyn: int
    bone_info_size: int
    num_streams: int
    info: Ms2Root
    buffer_pointers: Array[BufferPresence]
    mdl_2_names: Array[str]
    modelstream_names: Array[str]
    buffer_0: Buffer0
    buffer_infos: Array[BufferInfo]
    model_infos: Array[ModelInfo]
    models_reader: ModelReader

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
