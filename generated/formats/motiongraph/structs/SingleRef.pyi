from typing import Generic, TypeVar
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Reference import Reference


_T = TypeVar("_T")

class SingleRef(MemStruct, Generic[_T]):
    pointer: Reference[_T]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
