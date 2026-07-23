
# START_GLOBALS
from generated.array import Array
from generated.formats.ms2.structs.MeshData import MeshData
from generated.formats.ms2.structs.TriChunk import TriChunk
from generated.formats.ms2.structs.VertChunk import VertChunk
# END_GLOBALS

class ChunkedMesh(MeshData):
    # START_VARS
    vert_chunks: Array[VertChunk]
    tri_chunks: Array[TriChunk]
    # END_VARS

    # START_CLASS