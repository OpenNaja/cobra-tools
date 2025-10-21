from generated.base_struct import BaseStruct


class Vector2(BaseStruct):
    x: float
    y: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
