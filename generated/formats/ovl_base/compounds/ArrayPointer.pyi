from typing import TypeVar
from generated.array import Array
from generated.formats.ovl_base.compounds.Pointer import Pointer


_T = TypeVar("_T")

class ArrayPointer(Pointer[Array[_T]]):
    pass

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
