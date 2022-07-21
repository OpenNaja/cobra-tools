
UBYTE_SCALE = 128
UBYTE_MAX = 255
USHORT_SCALE = 2048
USHORT_OFFSET = 32766.5
USHORT_MIN = 0
USHORT_MAX = 65535
PACKEDVEC_MAX = 2 ** 20  # 0x100000
FUR_OVERHEAD = 2


def unpack_ushort_vector(vec):
    return (vec - USHORT_OFFSET) / USHORT_SCALE


def unpack_swizzle(vec):
    # swizzle to avoid a matrix multiplication for global axis correction
    return -vec[0], -vec[2], vec[1]


def unpack_swizzle_vectorized(arr):
    arr[:] = arr[:, (0, 2, 1)]
    arr[:, (0, 1)] *= -1.0


def pack_swizzle(vec):
    # swizzle to avoid a matrix multiplication for global axis correction
    return -vec[0], vec[2], -vec[1]


def pack_swizzle_vectorized(arr):
    arr[:] = arr[:, (0, 2, 1)]
    arr[:, (0, 2)] *= -1.0


def ushort_clamp(coord):
    return max(min(coord, USHORT_MAX), USHORT_MIN)


def pack_ushort_vector(vec):
    return [ushort_clamp(int(round(coord * USHORT_SCALE + USHORT_OFFSET))) for coord in vec]


def pack_ubyte_vector(vec):
    return [min(int(round(x * UBYTE_SCALE + UBYTE_SCALE)), UBYTE_MAX) for x in vec]


def scale_unpack(f, base):
    """Converts a packed int component into a float in the range specified by base"""
    scale = base / PACKEDVEC_MAX
    return (f + base) * scale


def scale_pack(f, base):
    """Packs a float into the range specified by base"""
    scale = base / PACKEDVEC_MAX
    return int(round(f / scale - base))


def unpack_longint_vec(input, base):
    """Unpacks and returns the self.raw_pos uint64"""
    # numpy uint64 does not like the bit operations so we cast to default int
    input = int(input)
    output = []
    # print("inp",bin(input))
    for i in range(3):
        # print("\nnew coord")
        # grab the last 20 bits with bitand
        # bit representation: 0b11111111111111111111
        twenty_bits = input & 0xFFFFF
        # print("input", bin(input))
        # print("twenty_bits = input & 0xFFFFF ", bin(twenty_bits), twenty_bits)
        input >>= 20
        # print("input >>= 20", bin(input))
        # print("1",bin(1))
        # get the rightmost bit
        rightmost_bit = input & 1
        # print("rightmost_bit = input & 1",bin(rightmost_bit))
        # print(rightmost_bit, twenty_bits)
        if not rightmost_bit:
            # rightmost bit was 0
            # print("rightmost_bit == 0")
            # bit representation: 0b100000000000000000000
            twenty_bits -= PACKEDVEC_MAX
        # print("final int", twenty_bits)
        output.append(scale_unpack(twenty_bits, base))
        # shift to skip the sign bit
        input >>= 1
    # input at this point is either 0 or 1
    return output, input


def pack_longint_vec(vec, residue, base):
    """Packs the input vector + residue bit into a uint64 (1, 21, 21, 21)"""
    output = 0
    for i, f in enumerate(vec):
        o = scale_pack(f, base)
        # print("restored int", o)
        # we are 'clamping' here if we - essentially wrapping the range around
        # probably not correct!
        # i think the cond might be o < 0
        if o < PACKEDVEC_MAX:
            # 0b100000000000000000000
            o += PACKEDVEC_MAX
        else:
            # set the 1 bit flag
            output |= 1 << (21 * (i + 1) - 1)
        # print("restored int + correction", o)
        output |= o << (21 * i)
    # print("bef",bin(output))
    output |= residue << 63
    return output


def get_valid_weights(vert):
    return [(b, w / 255) for b, w in zip(vert["bone ids"], vert["bone weights"]) if w > 0]


def unpack_weights(model, i):
    # weight in range 0-1
    weights = []
    if hasattr(model, "weights_data"):
        weights = get_valid_weights(model.weights_data[i])
    elif "bone ids" in model.dt.fields:
        weights = get_valid_weights(model.verts_data[i])
    if not weights:
        # fallback: skin partition
        weights = [(model.verts_data[i]["bone index"], 1.0), ]
    return weights


def remap(v, old_min, old_max, new_min, new_max):
    return ((v - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
