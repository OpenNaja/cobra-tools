from generated.base_struct import BaseStruct


class Repeat2(BaseStruct):
    ind: int
    a: int
    b: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
