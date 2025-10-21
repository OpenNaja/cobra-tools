from generated.base_struct import BaseStruct


class BufferGroup(BaseStruct):
    buffer_offset: int
    buffer_count: int
    ext_index: int
    buffer_index: int
    size: int
    data_offset: int
    data_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
