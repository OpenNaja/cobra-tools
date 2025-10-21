from generated.base_struct import BaseStruct


class AkPathListItemOffset(BaseStruct):
    ul_vertices_offset: int
    i_num_vertices: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
