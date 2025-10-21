from generated.base_struct import BaseStruct


class BufferEntry(BaseStruct):
    index: int
    size: int
    file_hash: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
