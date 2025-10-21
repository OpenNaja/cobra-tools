from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.compounds.PadAlign import PadAlign
from generated.formats.ms2.compounds.MeshCollisionOptimizer import MeshCollisionOptimizer
from generated.formats.ovl_base.compounds.Empty import Empty


class MeshCollisionData(BaseStruct):
    optimizer: MeshCollisionOptimizer
    vertices_addr: Empty
    vertices: Array[Array[float]]
    triangles_addr: Empty
    triangles: Array[Array[int]]
    const: int
    triangle_flags: Array[int]
    triangle_flags_pc: Array[Array[int]]
    mesh_aligner: PadAlign[object]
    zero_end: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
