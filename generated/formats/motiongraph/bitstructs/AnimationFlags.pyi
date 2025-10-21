from generated.bitfield import BasicBitfield


class AnimationFlags(BasicBitfield):
    looping: int
    additive: int
    mirrored: int
    affects_motion: int
    flag_on_loop: int
    reset_random_on_loop: int
    suppress_resource_data_streams: int
