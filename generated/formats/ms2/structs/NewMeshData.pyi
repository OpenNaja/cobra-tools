from generated.formats.ms2.bitfields.ModelFlag import ModelFlag
from generated.formats.ms2.structs.MeshData import MeshData


class NewMeshData(MeshData):
    vertex_count: int
    tri_index_count: int
    zero_1: int
    poweroftwo: int
    vertex_offset: int
    size_of_vertex: int
    tri_offset: int
    zero_2: int
    unk_float_0: float
    unk_float_1: float
    zero_3: int
    flag: ModelFlag

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
