import numpy as np
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bani.structs.BaniGpuChannelBones import BaniGpuChannelBones
from generated.formats.base.structs.PadAlignFF import PadAlignFF
from generated.formats.ovl_base.structs.Empty import Empty


class BaniGpuChannelsLod(BaseStruct):
    ref: Empty
    data: np.ndarray[tuple[int], np.dtype[BaniGpuChannelBones]]
    padding: PadAlignFF[object]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
