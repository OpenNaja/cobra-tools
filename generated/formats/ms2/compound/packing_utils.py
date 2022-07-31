import numpy as np

UBYTE_SCALE = 127
UBYTE_MAX = 255
USHORT_SCALE = 2048
USHORT_SCALE_B = 65536
USHORT_OFFSET = 32766.5
USHORT_MIN = 0
USHORT_MAX = 65535
PACKEDVEC_MAX = 2 ** 20 - 1  # 0x100000
# PACKEDVEC_MAX = 2 ** 20  # 0x100000
FUR_OVERHEAD = 2
zero_uint64 = np.uint64(0)


def unpack_ubyte_vector(arr, normalize=True):
    # convert to +-1 range; 255 is unused
    arr[:] = arr / UBYTE_SCALE - 1.0
    # some cases (oct) do not use normalization after unpacking
    if normalize:
        arr /= np.linalg.norm(arr, axis=1, keepdims=True)


def pack_ubyte_vector(arr):
    arr[:] = np.round(arr * UBYTE_SCALE + UBYTE_SCALE)


def unpack_ushort_vector(arr):
    arr[:] = (arr - USHORT_OFFSET) / USHORT_SCALE


def unpack_ushort_vector_b(arr):
    arr[:] = arr / USHORT_SCALE_B


def pack_ushort_vector(arr):
    arr[:] = np.round(arr * USHORT_SCALE + USHORT_OFFSET)


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


def scale_unpack_vectorized(f, base):
    """Converts a packed int component into a float in the range specified by base"""
    f[:] = (f + base) * base / PACKEDVEC_MAX - base


def scale_pack_vectorized(f, base):
    """Packs a float into the range specified by base"""
    f[:] = np.round((f + base) / base * PACKEDVEC_MAX - base)


def unpack_int64_vector(packed_vert, vertices, use_blended_weights):
    for i in range(3):
        # grab the last 21 bits with bitand
        twentyone_bits = packed_vert & 0b111111111111111111111
        packed_vert >>= 21
        vertices[:, i] = twentyone_bits
    use_blended_weights[:] = packed_vert


def pack_int64_vector(packed_vert, vertices, use_blended_weights):
    packed_vert[:] = 0
    for i in range(3):
        packed_vert |= vertices[:, i] << (21 * i)
    packed_vert |= use_blended_weights.astype(np.int64) << 63


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


def sign_not_zero(a):
    # 	vec2 signNotZero(vec2 v) {
    # return vec2((v.x >= 0.0) ? +1.0 : -1.0, (v.y >= 0.0) ? +1.0 : -1.0);
    # }
    # np.sign returns -1 if x < 0, 0 if x==0, 1 if x > 0
    c = a.copy()
    c[:] = -1.0
    c[a >= 0.0] = 1.0
    return c


def vec3_to_oct(arr):
    # ported from Cigolle et al. "Survey of Efficient Representations for Independent Unit Vectors" 2014.
    # // Assume normalized input. Output is on [-1, 1] for each component.
    # vec2 float32x3_to_oct(in vec3 v) {
    # // Project the sphere onto the octahedron, and then onto the xy plane
    # vec2 p = v.xy * (1.0 / (abs(v.x) + abs(v.y) + abs(v.z)));
    # // Reflect the folds of the lower hemisphere over the diagonals
    # return (v.z <= 0.0) ? ((1.0 - abs(p.yx)) * signNotZero(p)) : p;
    # }
    # Project the sphere onto the octahedron, and then onto the xy plane
    arr[:, (0, 1)] /= np.sum(np.abs(arr), axis=1, keepdims=True)
    # Reflect the folds of the lower hemisphere over the diagonals
    # update xy when z <= 0
    arr[arr[:, 2] <= 0.0, :2] = ((1.0 - np.abs(arr[:, (1, 0)])) * sign_not_zero(arr[:, (0, 1)]))[arr[:, 2] <= 0.0, :2]
    pack_ubyte_vector(arr)
    # clear z coord
    arr[:, 2] = 0.0


def oct_to_vec3(arr):
    # ported from Cigolle et al. "Survey of Efficient Representations for Independent Unit Vectors" 2014.
    # vec3 oct_to_float32x3(vec2 e) {
    # vec3 v = vec3(e.xy, 1.0 - abs(e.x) - abs(e.y));
    # if (v.z < 0) v.xy = (1.0 - abs(v.yx)) * signNotZero(v.xy);
    # return normalize(v);
    # }
    unpack_ubyte_vector(arr, normalize=False)
    arr[:, 2] = 1.0 - np.abs(arr[:, 0]) - np.abs(arr[:, 1])
    # note that advanced indexing like this creates a copy instead of a view, which makes this messy
    arr[arr[:, 2] < 0, 0:2] = ((1.0 - np.abs(arr[:, (1, 0)])) * sign_not_zero(arr[:, :2]))[arr[:, 2] < 0]
    # normalize after conversion
    arr /= np.linalg.norm(arr, axis=1, keepdims=True)
