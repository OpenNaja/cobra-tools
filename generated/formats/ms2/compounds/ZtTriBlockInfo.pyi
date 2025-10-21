from generated.base_struct import BaseStruct


class ZtTriBlockInfo(BaseStruct):
    tri_index_count: int
    a: int
    unk_index: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
