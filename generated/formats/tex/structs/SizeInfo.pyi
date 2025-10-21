from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.tex.structs.SizeInfoRaw import SizeInfoRaw


class SizeInfo(MemStruct):
    data: SizeInfoRaw
    padding: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
