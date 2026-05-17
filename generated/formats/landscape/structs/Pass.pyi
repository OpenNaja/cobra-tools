from generated.base_struct import BaseStruct


class Pass(BaseStruct):
    name_offset: int
    a: int
    b: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
