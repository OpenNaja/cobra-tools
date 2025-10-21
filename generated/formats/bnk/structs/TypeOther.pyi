from generated.array import Array
from generated.formats.bnk.structs.HircObject import HircObject


class TypeOther(HircObject):
    raw: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
