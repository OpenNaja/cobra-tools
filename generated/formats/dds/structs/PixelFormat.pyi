from generated.base_struct import BaseStruct
from generated.formats.dds.bitstructs.PixelFormatFlags import PixelFormatFlags
from generated.formats.dds.enums.FourCC import FourCC


class PixelFormat(BaseStruct):
    size: int
    flags: PixelFormatFlags
    four_c_c: FourCC
    bit_count: int
    r_mask: int
    g_mask: int
    b_mask: int
    a_mask: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
