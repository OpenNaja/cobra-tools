from typing import Generic, TypeVar
from generated.base_struct import BaseStruct


_T = TypeVar("_T")

class Pointer(BaseStruct, Generic[_T]):
    pool_index: int
    data_offset: int
    data: _T

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
