from generated.bitfield import BasicBitfield


class ModelFlag(BasicBitfield):
    unk: int
    stripify: bool
    weights: bool
    repeat_tris: bool
    num_shells: int
    direct_address: bool
