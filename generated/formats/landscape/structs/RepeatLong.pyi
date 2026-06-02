from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.landscape.structs.Pair import Pair


class RepeatLong(BaseStruct):
    zero: int
    ind: int
    pair: Array[Pair]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
