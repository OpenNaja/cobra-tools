from typing import Union
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.PadAlign import PadAlign
from generated.formats.ms2.structs.IKEntry import IKEntry
from generated.formats.ms2.structs.IKEntryOld import IKEntryOld
from generated.formats.ms2.structs.IKTarget import IKTarget
from generated.formats.ovl_base.structs.Empty import Empty
from generated.formats.ovl_base.structs.SmartPadding import SmartPadding


class IKInfo(BaseStruct):
    weird_padding: SmartPadding
    ik_count: int
    ik_ptr: int
    ik_targets_count: int
    ik_targets_ptr: int
    ik_ref: Empty
    ik_list: Union[Array[IKEntryOld], Array[IKEntry]]
    padding_0: PadAlign[object]
    ik_targets: Array[IKTarget]
    padding_1: PadAlign[object]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
