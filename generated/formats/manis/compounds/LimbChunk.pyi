from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.compounds.WeirdElementOne import WeirdElementOne
from generated.formats.manis.compounds.WeirdElementTwoReader import WeirdElementTwoReader


class LimbChunk(BaseStruct):
    list_one: Array[WeirdElementOne]
    list_two: WeirdElementTwoReader

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
