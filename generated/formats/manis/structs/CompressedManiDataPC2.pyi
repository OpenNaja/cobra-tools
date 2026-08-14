from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.PadAlign import PadAlign


class CompressedManiDataPC2(BaseStruct):
    size: int
    acl_data: Array[int]
    pad: PadAlign[object]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
