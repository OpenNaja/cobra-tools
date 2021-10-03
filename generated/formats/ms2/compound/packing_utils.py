USHORT_SCALE = 2048
USHORT_OFFSET = 32766.5
USHORT_MIN = 0
USHORT_MAX = 65535
PACKEDVEC_MAX = 2 ** 20  # 0x100000


def unpack_ushort_vector(vec):
    return (vec - USHORT_OFFSET) / USHORT_SCALE


def unpack_swizzle(vec):
    # swizzle to avoid a matrix multiplication for global axis correction
    return -vec[0], -vec[2], vec[1]


def pack_swizzle(vec):
    # swizzle to avoid a matrix multiplication for global axis correction
    return -vec[0], vec[2], -vec[1]


def ushort_clamp(coord):
    return max(min(coord, USHORT_MAX), USHORT_MIN)


def pack_ushort_vector(vec):
    return [ushort_clamp(int(round(coord * USHORT_SCALE + USHORT_OFFSET))) for coord in vec]


def pack_ubyte_vector(vec):
    return [min(int(round(x * 128 + 128)), 255) for x in vec]


def scale(base):
    return base / PACKEDVEC_MAX


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
        output.append(twenty_bits * scale(base))
        # shift to skip the sign bit
        input >>= 1
    # input at this point is either 0 or 1
    return output, input


def pack_longint_vec(vec, residue, base):
    """Packs the input vector + residue bit into a uint64 (1, 21, 21, 21)"""
    output = 0
    for i, f in enumerate(vec):
        o = int(round(f / scale(base)))
        # print("restored int", o)
        # we are 'clamping' here if we - essentially wrapping the range around
        # probably not correct!
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
    # thing = struct.unpack("<d", struct.pack("<Q",output))
    # thing2 = -1.0*float(thing[0])
    # output = struct.unpack("<Q", struct.pack("<d",thing2))[0]
    return output


def unpack_weights(model, i, residue, extra=True):
    vert_w = []
    if "bone ids" in model.dt.fields:
        vert_w = [(i, w) for i, w in zip(model.verts_data[i]["bone ids"], model.verts_data[i]["bone weights"]) if w > 0]
    elif hasattr(model, "weights_data"):
        vert_w = [(i, w) for i, w in zip(model.weights_data[i]["bone ids"], model.weights_data[i]["bone weights"]) if
                  w > 0]
    if extra:
        # fallback: skin parition
        if not vert_w:
            vert_w = [(model.verts_data[i]["bone index"], 255), ]

        # create fur length vgroup
        if model.fur is not None:
            vert_w.append(("fur_length", model.fur[i][0] * 255))
            vert_w.append(("fur_width", model.fur[i][1] * 255))

        # the unknown 0, 128 byte
        vert_w.append(("unk0", model.verts_data[i]["unk"] * 255))
        # packing bit
        vert_w.append(("residue", residue * 255))
    return vert_w


def remap(v, old_min, old_max, new_min, new_max):
    return ((v - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
