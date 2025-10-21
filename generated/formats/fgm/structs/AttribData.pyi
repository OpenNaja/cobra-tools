from typing import Union
from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class AttribData(MemStruct):
    value: Union[Array[float], Array[int]]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
