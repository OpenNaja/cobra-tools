from typing import Generic, TypeVar
from generated.array import Array
from generated.base_struct import BaseStruct


_T = TypeVar("_T")

class DataSlot(BaseStruct, Generic[_T]):
    _offset: int
    _count: int
    data: Array[_T]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
