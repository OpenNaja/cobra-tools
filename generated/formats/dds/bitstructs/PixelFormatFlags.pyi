from generated.bitfield import BasicBitfield


class PixelFormatFlags(BasicBitfield):
    alpha_pixels: int
    alpha: int
    four_c_c: int
    palette_indexed_4: int
    reserved_1: int
    palette_indexed_8: int
    rgb: int
    reserved_2: int
    palette_indexed_1: int
    palette_indexed_2: int
    reserved_3: int
    alpha_premult: int
    reserved_4: int
    luminance: int
    reserved_5: int
    normal: int
