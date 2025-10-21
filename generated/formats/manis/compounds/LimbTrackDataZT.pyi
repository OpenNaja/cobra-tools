from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.compounds.LimbChunkReaderZt import LimbChunkReaderZt
from generated.formats.manis.compounds.LimbInfoZT import LimbInfoZT
from generated.formats.ovl_base.compounds.Empty import Empty


class LimbTrackDataZT(BaseStruct):
    ref: Empty
    limb_count: int
    pad: int
    limbs: Array[LimbInfoZT]
    limbs_data: LimbChunkReaderZt

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
