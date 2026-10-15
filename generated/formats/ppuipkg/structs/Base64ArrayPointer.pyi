from typing import TypeVar
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer


_T = TypeVar("_T")

class Base64ArrayPointer(ArrayPointer[_T]):
    pass

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
