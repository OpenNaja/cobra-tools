from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.compounds.ElemZt import ElemZt


class LimbChunkZt(BaseStruct):
    list_one: Array[Array[float]]
    list_two: Array[ElemZt]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
