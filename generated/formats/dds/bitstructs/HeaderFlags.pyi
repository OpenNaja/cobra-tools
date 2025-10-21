from generated.bitfield import BasicBitfield


class HeaderFlags(BasicBitfield):
    caps: int
    height: int
    width: int
    pitch: int
    reserved_1: int
    pixel_format: int
    reserved_2: int
    mipmap_count: int
    reserved_3: int
    linear_size: int
    reserved_4: int
    depth: int
