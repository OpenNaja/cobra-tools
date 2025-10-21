from generated.array import Array
from generated.base_struct import BaseStruct


class WeirdElementTwo(BaseStruct):
    many_floats: Array[float]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
