from typing import Union
from generated.formats.ms2.bitfields.ModelFlagDLA import ModelFlagDLA
from generated.formats.ms2.bitfields.ModelFlagZT import ModelFlagZT
from generated.formats.ms2.structs.MeshData import MeshData


class ZtMeshData(MeshData):
    tri_index_count: int
    vertex_count: int
    tri_info_offset: int
    vert_info_offset: int
    known_ff_0: int
    tri_offset: int
    uv_offset: int
    vertex_offset: int
    unk_index: int
    one_0: int
    one_1: int
    poweroftwo: int
    flag: Union[ModelFlagDLA, ModelFlagZT]
    zero_uac: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
