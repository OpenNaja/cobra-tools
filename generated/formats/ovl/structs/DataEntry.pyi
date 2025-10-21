from generated.base_struct import BaseStruct


class DataEntry(BaseStruct):
    file_hash: int
    ext_hash: int
    set_index: int
    buffer_count: int
    zero: int
    size_1: int
    size_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
