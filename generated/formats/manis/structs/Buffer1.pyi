from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.PadAlign import PadAlign


class Buffer1(BaseStruct):
    target_hashes: Array[int]
    target_names: Array[str]
    bone_pad: PadAlign[object]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
