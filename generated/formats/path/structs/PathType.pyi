from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.path.enums.PathTypes import PathTypes


class PathType(MemStruct):
    enum_value: PathTypes
    _align: Array[int]
    min_width: float
    max_width: float
    _unk_int_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
