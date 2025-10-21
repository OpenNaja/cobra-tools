from generated.base_struct import BaseStruct


class StreamEntry(BaseStruct):
    stream_offset: int
    file_offset: int
    zero: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
