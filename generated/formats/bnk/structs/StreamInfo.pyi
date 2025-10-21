from generated.base_struct import BaseStruct


class StreamInfo(BaseStruct):
    offset: int
    size: int
    event_id: int
    zero: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
