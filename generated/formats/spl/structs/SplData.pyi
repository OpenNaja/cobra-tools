from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.spl.structs.Key import Key
from generated.formats.spl.structs.Vector3 import Vector3


class SplData(MemStruct):
    offset: Vector3
    scale: float
    keys: Array[Key]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
