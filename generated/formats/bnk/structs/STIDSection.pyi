from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.structs.STIDRef import STIDRef


class STIDSection(BaseStruct):
    length: int
    ui_type: int
    ui_size: int
    data_pointers: Array[STIDRef]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
