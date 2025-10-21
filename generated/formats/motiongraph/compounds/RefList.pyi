from typing import Generic, TypeVar
from generated.array import Array
from generated.formats.motiongraph.compounds.SingleRef import SingleRef
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


_T = TypeVar("_T")

class RefList(MemStruct, Generic[_T]):
    ptrs: Array[SingleRef[_T]]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
