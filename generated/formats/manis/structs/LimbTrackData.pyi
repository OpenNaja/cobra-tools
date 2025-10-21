from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.structs.LimbChunkReader import LimbChunkReader
from generated.formats.manis.structs.LimbInfo import LimbInfo
from generated.formats.ovl_base.structs.Empty import Empty
from generated.formats.ovl_base.structs.SmartPadding import SmartPadding


class LimbTrackData(BaseStruct):
    ref: Empty
    padding_0: SmartPadding
    limb_count: int
    flag: int
    zero_1: int
    limbs: Array[LimbInfo]
    limbs_data: LimbChunkReader

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
