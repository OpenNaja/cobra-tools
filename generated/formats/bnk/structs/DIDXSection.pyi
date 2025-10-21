from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.structs.DataPointer import DataPointer


class DIDXSection(BaseStruct):
    length: int
    data_pointers: Array[DataPointer]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
