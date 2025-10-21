from generated.formats.ms2.bitfields.ModelFlag import ModelFlag
from generated.formats.ms2.structs.MeshData import MeshData


class PcMeshData(MeshData):
    tri_index_count_a: int
    vertex_count: int
    tri_offset: int
    tri_index_count: int
    vertex_offset: int
    weights_offset: int
    uv_offset: int
    uv_offset_2: int
    vertex_color_offset: int
    vertex_offset_within_lod: int
    poweroftwo: int
    zero_b: int
    unk_float_0: float
    flag: ModelFlag
    zero_c: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
