from generated.base_struct import BaseStruct


class ZerosPadding(BaseStruct):
    padding_0: int
    padding_1: int
    padding_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
