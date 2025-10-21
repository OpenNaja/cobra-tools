from generated.base_struct import BaseStruct


class Area(BaseStruct):
    _id: int
    width_1: int
    height_1: int
    width_2: int
    height_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
