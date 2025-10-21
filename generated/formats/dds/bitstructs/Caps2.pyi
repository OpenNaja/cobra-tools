from generated.bitfield import BasicBitfield


class Caps2(BasicBitfield):
    reserved_1: int
    cubemap: int
    cubemap_pos_x: int
    cubemap_neg_x: int
    cubemap_pos_y: int
    cubemap_neg_y: int
    cubemap_pos_z: int
    cubemap_neg_z: int
    reserved_2: int
    volume: int
