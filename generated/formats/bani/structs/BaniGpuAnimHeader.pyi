from generated.base_struct import BaseStruct
from generated.formats.bani.bitfields.PackedOffsetBones import PackedOffsetBones


class BaniGpuAnimHeader(BaseStruct):
    uniform_scale: float
    uniform_bias: float
    packed_offset_bones: PackedOffsetBones
    keyframes_offset: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
