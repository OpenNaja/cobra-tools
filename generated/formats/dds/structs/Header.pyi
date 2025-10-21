from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.FixedString import FixedString
from generated.formats.dds.bitstructs.Caps1 import Caps1
from generated.formats.dds.bitstructs.Caps2 import Caps2
from generated.formats.dds.bitstructs.HeaderFlags import HeaderFlags
from generated.formats.dds.structs.Dxt10Header import Dxt10Header
from generated.formats.dds.structs.PixelFormat import PixelFormat


class Header(BaseStruct):
    header_string: FixedString
    size: int
    flags: HeaderFlags
    height: int
    width: int
    linear_size: int
    depth: int
    mipmap_count: int
    reserved_1: Array[int]
    pixel_format: PixelFormat
    caps_1: Caps1
    caps_2: Caps2
    caps_3: int
    caps_4: int
    unused: int
    dx_10: Dxt10Header

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
