from typing import Generic, TypeVar
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


_T = TypeVar("_T")

class SinglePtr(MemStruct, Generic[_T]):
    ptr: Pointer[_T]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
