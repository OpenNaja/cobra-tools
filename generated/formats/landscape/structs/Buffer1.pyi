from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.landscape.structs.Struct2 import Struct2


class Buffer1(BaseStruct):
    z_0: Array[int]
    unk_5: Array[Struct2]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
