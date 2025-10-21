from generated.formats.ms2.bitfields.ChunkedModelFlag import ChunkedModelFlag
from generated.formats.ms2.structs.MeshData import MeshData


class ChunkedMesh(MeshData):
    chunks_offset: int
    chunks_count: int
    tris_count: int
    vertex_count: int
    zero: int
    poweroftwo: int
    unk_float_0: float
    unk_float_1: float
    flag: ChunkedModelFlag

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
