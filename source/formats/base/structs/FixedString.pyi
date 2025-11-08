from generated.base_struct import BaseStruct


class FixedString(BaseStruct):
    data: bytes

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
