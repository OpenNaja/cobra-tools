def unpack_ushort_vector(vec):
    return (vec - 32768) / 2048


def unpack_swizzle(vec):
    # swizzle to avoid a matrix multiplication for global axis correction
    return -vec[0], -vec[2], vec[1]


def pack_swizzle(vec):
    # swizzle to avoid a matrix multiplication for global axis correction
    return -vec[0], vec[2], -vec[1]


def pack_ushort_vector(vec):
    return [min(int(round(coord * 2048 + 32768)), 65535) for coord in vec]


def pack_ubyte_vector(vec):
    return [min(int(round(x * 128 + 128)), 255) for x in vec]


def unpack_longint_vec(input, base):
    """Unpacks and returns the self.raw_pos uint64"""
    # numpy uint64 does not like the bit operations so we cast to default int
    input = int(input)
    # correct for size according to base, relative to 512
    scale = base / 512 / 2048
    # input = self.raw_pos
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
            twenty_bits -= 0x100000
        # print("final int", twenty_bits)
        o = (twenty_bits + base) * scale
        output.append(o)
        # shift to skip the sign bit
        input >>= 1
    # input at this point is either 0 or 1
    return output, input


def pack_longint_vec(vec, residue, base):
    """Packs the input vector + residue bit into a uint64 (1, 21, 21, 21)"""
    # correct for size according to base, relative to 512
    scale = base / 512 / 2048
    output = 0
    for i, f in enumerate(vec):
        o = int(round(f / scale - base))
        # print("restored int", o)
        if o < 0x100000:
            # 0b100000000000000000000
            o += 0x100000
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
