from generated.bitfield import BasicBitfield


class TurnFlags(BasicBitfield):
    looping: int
    clockwise: int
    use_midpoint: int
