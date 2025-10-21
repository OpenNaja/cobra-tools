from generated.base_struct import BaseStruct


class BufferInfo(BaseStruct):
    u_0: int
    u_1: int
    tri_chunks_size: int
    tri_chunks_ptr: int
    vert_chunks_size: int
    vert_chunks_ptr: int
    verts_size: int
    verts_ptr: int
    u_3: int
    tris_size: int
    tris_ptr: int
    u_5: int
    u_6: int
    u_5: int
    uvs_size: int
    u_6: int
    u_7: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
