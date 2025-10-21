from generated.base_struct import BaseStruct


class Fragment(BaseStruct):
    link_pool: int
    link_offset: int
    struct_pool: int
    struct_offset: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
