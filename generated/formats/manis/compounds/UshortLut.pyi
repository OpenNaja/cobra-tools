from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.ovl_base.compounds.Empty import Empty
from generated.formats.ovl_base.compounds.SmartPadding import SmartPadding


class UshortLut(BaseStruct):
    ref: Empty
    align: SmartPadding
    a: Array[int]
    b: Array[int]
    zeros: Array[int]
    target_bone_count: int
    offsets: Array[int]
    flags: Array[int]
    ref_2: Empty

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
