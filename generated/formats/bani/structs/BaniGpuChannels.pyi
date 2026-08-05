import BaniChannelBones
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.PadAlign import PadAlign
from generated.formats.ovl_base.structs.Empty import Empty


class BaniGpuChannels(BaseStruct):
    ref: Empty
    data: Array[BaniChannelBones]
    padding: PadAlign[object]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
