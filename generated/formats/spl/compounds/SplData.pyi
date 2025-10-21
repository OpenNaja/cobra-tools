from generated.array import Array
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.spl.compounds.Key import Key
from generated.formats.spl.compounds.Vector3 import Vector3


class SplData(MemStruct):
    offset: Vector3
    scale: float
    keys: Array[Key]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
