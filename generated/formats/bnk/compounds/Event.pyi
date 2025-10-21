from generated.array import Array
from generated.formats.bnk.compounds.HircObject import HircObject


class Event(HircObject):
    num_actions: int
    children: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
