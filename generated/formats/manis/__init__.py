from generated.formats.manis.imports import name_type_map
import logging
import os
import time
from copy import copy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import matplotlib

import numpy as np

np.seterr(all='warn')
# np.seterr(all='print')
np.set_printoptions(precision=4, suppress=True)

from generated.io import IoFile
from generated.formats.manis.bitfields.ManisDtype import ManisDtype
from generated.formats.manis.bitfields.StoreKeys import StoreKeys
from generated.formats.manis.structs.InfoHeader import InfoHeader
from generated.formats.manis.versions import get_game, set_game
from modules.formats.shared import djb2

COMPONENT_BITS = 15
SEGMENT_FRAME_COUNT = 32
QUANT_MIN = np.float32(128.0)
QUANT_MAX = np.float32(16383.0)
PACK_SCALE = np.float32(1.0) / QUANT_MAX
ROTATION_VECTOR_SCALE = np.float32(2.0 * np.pi) * PACK_SCALE
FLOAT32_EPSILON = np.finfo(np.float32).eps

try:
    import bitarray
    import bitarray.util


    class BinStream:
        def __init__(self, val: bytes):
            self.data = bitarray.bitarray(endian='little')
            self.data.frombytes(val)
            self.pos = 0

        def seek(self, pos: int):
            self.pos = pos

        def read(self, size: int) -> bitarray.bitarray:
            d = self.data[self.pos: self.pos + size]
            if len(d) != size:
                raise EOFError(
                    f"Reached end of chunk reading {size} bits at bit {self.pos}, "
                    f"byte {self.pos / 8}, got {len(d)} bits"
                )
            self.pos += size
            return d

        def read_int(self, size: int) -> int:
            bits = self.read(size)
            return bitarray.util.ba2int(bits, signed=True)

        def read_uint(self, size: int) -> int:
            bits = self.read(size)
            return bitarray.util.ba2int(bits, signed=False)

        def read_uint_reversed(self, size: int) -> int:
            bits = self.read(size)
            bits.reverse()
            return bitarray.util.ba2int(bits, signed=False)

        def read_unary_count(self, max_size: int) -> int:
            for rel_size in range(max_size):
                if not self.read_uint(1):
                    return rel_size
            raise ValueError(f"Unary value exceeds its {max_size}-bit limit")

        @staticmethod
        def decode_zigzag(*values: int) -> list[int]:
            return [-(value + 1 >> 1) if value & 1 else value >> 1 for value in values]

        def find_all(self, bits):
            for match_offset in self.data.itersearch(bits):
                yield match_offset

except ImportError:
    BinStream = None
    logging.warning("bitarray module is not installed")


POS = "pos"
ORI = "ori"
SCL = "scl"
FLO = "float"
EUL = "euler"
root_name = "def_c_root_joint"
srb_name = "srb"


def clamp_normalized_vector(vec: np.ndarray) -> np.ndarray:
    """Clamp a normalized codec vector to the native signed-unit range."""
    return np.asarray(np.clip(vec, -1.0, 1.0), dtype=np.float32)


def has_stored_keys(keys_flag: StoreKeys) -> bool:
    """Return whether any X/Y/Z relative-key stream is present."""
    return bool(keys_flag.x or keys_flag.y or keys_flag.z)


def get_rotation_pack_scale(quantisation_level: int, norm: float) -> np.float32:
    """Return the native rotation scale for the following relative key.

    The decoder only selects its dynamic quantisation factor for a relative
    vector norm strictly inside (0, 0.5). All other norms use 1 / 16383.
    """
    norm = np.float32(np.clip(np.float32(norm), np.float32(0.0), np.float32(1.0)))
    if not (np.float32(0.0) < norm < np.float32(0.5)):
        return PACK_SCALE
    quant_factor = np.float32(quantisation_level) / norm
    quant_factor = np.float32(np.clip(quant_factor, QUANT_MIN, QUANT_MAX))
    return np.float32(1.0) / quant_factor


def get_quat_scale_fac(half_angle: float) -> tuple[np.float32, np.float32]:
    """Return ``(cos(half_angle), sin(half_angle))`` as float32 values.

    The native helper uses a range-reduced SIMD polynomial, but its semantic
    result is ordinary sine and cosine. NumPy already applies quadrant signs;
    no additional octant sign correction is appropriate.
    """
    angle = np.float32(half_angle)
    return np.float32(np.cos(angle)), np.float32(np.sin(angle))


def axis_angle_vector_to_quaternion(vec: np.ndarray) -> np.ndarray:
    """Convert an XYZ rotation vector to an XYZW unit quaternion."""
    angle = np.float32(np.linalg.norm(vec[:3]))
    if angle <= FLOAT32_EPSILON:
        return np.array((0.0, 0.0, 0.0, 1.0), dtype=np.float32)
    cos_half, sin_half = get_quat_scale_fac(np.float32(0.5) * angle)
    quat = np.zeros(4, dtype=np.float32)
    quat[:3] = np.asarray(vec[:3], dtype=np.float32) * (sin_half / angle)
    quat[3] = cos_half
    return quat


def multiply_quaternions(q1: np.ndarray, q2: np.ndarray) -> np.ndarray:
    """Return the Hamilton product ``q1 * q2`` for XYZW quaternions."""
    x1, y1, z1, w1 = q1
    x2, y2, z2, w2 = q2
    return np.array(
        (
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
        ),
        dtype=np.float32,
    )


def reconstruct_relative_quaternion(relative_xyz: np.ndarray) -> np.ndarray:
    """Reconstruct the fixed, non-negative W omitted by the relative format."""
    relative = np.zeros(4, dtype=np.float32)
    relative[:3] = np.asarray(relative_xyz[:3], dtype=np.float32)
    xyz_length_sq = np.float32(np.dot(relative[:3], relative[:3]))
    relative[3] = np.sqrt(np.maximum(np.float32(0.0), np.float32(1.0) - xyz_length_sq))
    return relative


def normalize_quaternion_or_identity(quat: np.ndarray) -> np.ndarray:
    """Normalize a quaternion, using identity for the native zero-length case."""
    norm = np.float32(np.linalg.norm(quat))
    if norm == np.float32(0.0):
        return np.array((0.0, 0.0, 0.0, 1.0), dtype=np.float32)
    return np.asarray(quat / norm, dtype=np.float32)


class KeysContext:
    def __init__(self, stream: BinStream, segment_frames_count: int):
        self.stream = stream
        self.do_increment = False
        self.runs_left = 0
        self.init_k_a = 0
        self.init_k_b = 0
        self.frames_left = 0
        self.begun = False

        # The first ushort is a byte offset to the shared frame-map stream.
        context_offset = stream.read_uint_reversed(16) * 8
        logging.debug(f"Context starts at bit {context_offset}")
        self.stream.seek(context_offset)
        if segment_frames_count == 1:
            if len(self.stream.data) == context_offset:
                logging.debug("Stream has no relative-key context")
            else:
                # A one-frame segment may contain an explicit empty context.
                empty = self.stream.read_uint(16)
                assert empty == 0, "Stream with no relative keys must have 00 00 context"
        else:
            self.do_increment = bool(self.stream.read_uint(1))
            self.runs_left = self.stream.read_uint(16)
            self.init_k_a = self.stream.read_uint_reversed(4)
            self.init_k_b = self.stream.read_uint_reversed(4)
            if not self.do_increment:
                self.init_k_a, self.init_k_b = self.init_k_b, self.init_k_a
            logging.debug(self)
            self.do_increment = not self.do_increment
            self.begun = True
        self.frame_map_offset = stream.pos
        stream.seek(16)

    def read_golomb_rice_data(
        self,
        segment_frames_count: int,
        keys_flag: StoreKeys,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Decode per-axis deltas and the shared stored-frame mask."""
        raw_keys = np.zeros((segment_frames_count, 3), dtype=np.int32)
        stored_frames = np.zeros(segment_frames_count, dtype=np.bool_)
        keys_offset = self.stream.pos

        self.stream.seek(self.frame_map_offset)
        for frame_i in range(1, segment_frames_count):
            if self.frames_left == 0:
                if self.runs_left == 0:
                    raise ValueError("Frame-map run stream ended before the segment")
                self.runs_left -= 1
                self.do_increment = not self.do_increment
                init_k = self.init_k_a if self.do_increment else self.init_k_b
                self.frames_left = self.decode_adaptive_golomb(init_k, 32 - init_k)
            self.frames_left -= 1
            if self.do_increment:
                stored_frames[frame_i] = True

        self.frame_map_offset = self.stream.pos
        self.stream.seek(keys_offset)
        for channel_i, is_active in enumerate((keys_flag.x, keys_flag.y, keys_flag.z)):
            if is_active:
                base_size = self.stream.read_uint_reversed(4)
                for target_frame in np.flatnonzero(stored_frames):
                    result = self.decode_adaptive_golomb(base_size, 32) & 0xffff
                    raw_keys[target_frame, channel_i] = self.stream.decode_zigzag(result)[0]
        return raw_keys, stored_frames

    def decode_adaptive_golomb(self, base_size: int, rel_size_limit: int) -> int:
        if not 0 <= base_size < 32:
            raise ValueError(f"Invalid Golomb base size: {base_size}")
        rel_size = self.stream.read_unary_count(rel_size_limit)
        offset = (1 << (base_size & 31)) * ((1 << rel_size) - 1)
        total_size = min(base_size + rel_size, COMPONENT_BITS)
        rel_key = self.stream.read_uint_reversed(total_size) if total_size else 0
        return offset + rel_key

    def __repr__(self):
        return (
            f"KeysContext(do_increment={self.do_increment}, runs_left={self.runs_left}, "
            f"init_k_a={self.init_k_a}, init_k_b={self.init_k_b})"
        )


class ManisFile(InfoHeader, IoFile):

    def __init__(self):
        super().__init__(self)
        self.context.bones_lut = {}


    @property
    def game(self):
        return get_game(self.context)[0].value

    @game.setter
    def game(self, game_name):
        set_game(self.context, game_name)
        set_game(self, game_name)

    def name_used(self, new_name):
        return any(mani.name == new_name for mani in self.mani_infos)

    def rename_file(self, old, new):
        logging.info(f"Renaming .mani in {self.name}")
        for mani in self.mani_infos:
            if mani.name == old:
                mani.name = new

    @staticmethod
    def get_max_v(mani_info):
        # BoneIndex in ManiInfo and bone arrays in ManiBlock use different ways to handle it in our code, but both are affected
        return 65535 if mani_info.dtype.use_ushort else 255

    def remove_bone(self, mani_name, dtype, bone_name):
        logging.info(f"Removing {bone_name} [{dtype}] from {mani_name}")
        for mani in self.mani_infos:
            if mani.name == mani_name:
                if mani.dtype.compression == 1:
                    logging.warning(f"{mani_name} is compressed, decompressing before editing")
                    self.force_decompress(mani)
                max_bone_index = self.get_max_v(mani)
                dtype_bare = dtype.replace("_bones", "")
                names = getattr(mani.keys, f"{dtype}_names")
                if len(names):
                    root_bone_name = ""
                    if dtype_bare in ("ori", "pos"):
                        root_index = getattr(mani, f"root_{dtype_bare}_bone")
                        if root_index != max_bone_index:
                            root_bone_name = names[root_index]

                    remove_i = names.index(bone_name)
                    names2 = names[:remove_i] + names[remove_i + 1:]
                    names.shape = (len(names2), )
                    names[:] = names2

                    if dtype_bare in (POS, ORI, SCL):
                        for s in (f"{dtype_bare}_bone_count", f"{dtype_bare}_bone_count_repeat", f"{dtype_bare}_bone_count_related"):
                            setattr(mani, s, len(names))
                        self.delete_from_array(f"{dtype_bare}_channel_to_bone", mani, remove_i, 0)
                    elif dtype_bare == "floats":
                        setattr(mani, "float_count", len(names))
                    self.delete_from_array(dtype, mani, remove_i, 1)
                    # update root bone index
                    root_index = names.index(root_bone_name) if root_bone_name in names else max_bone_index
                    setattr(mani, f"root_{dtype_bare}_bone", root_index)

    def delete_from_array(self, field_name, mani, remove_i, axis):
        keys = getattr(mani.keys, field_name)
        mani.keys.reset_field(field_name)
        keys2 = getattr(mani.keys, field_name)
        keys2[:] = np.delete(keys, remove_i, axis=axis)

    def remove(self, mani_names):
        logging.info(f"Removing {len(mani_names)} .mani files in {self.name}")
        for mani in reversed(self.mani_infos):
            if mani.name in mani_names:
                self.mani_infos.remove(mani)

    def duplicate(self, mani_names):
        logging.info(f"Duplicating {len(mani_names)} .mani files in {self.name}")
        for mani in reversed(self.mani_infos):
            if mani.name in mani_names:
                mani_copy = copy(mani)
                # add as many suffixes as needed to make new_name unique
                self.make_name_unique(mani_copy)
                self.mani_infos.append(mani_copy)
        self.mani_infos.sort(key=lambda mani: mani.name)

    def make_name_unique(self, mani_copy):
        new_name = mani_copy.name
        while self.name_used(new_name):
            new_name = f"{new_name}_copy"
        mani_copy.name = new_name

    def resize(self, fac):
        for mi in self.mani_infos:
            k = mi.keys
            if mi.dtype.compression != 0:
                ck = k.compressed
                ck.loc_bounds.mins *= fac
                ck.loc_bounds.scales *= fac
            else:
                k.pos_bones *= fac
            for bone_i, name in enumerate(k.floats_names):
                # typical dino float tracks:
                # def_c_head_joint.BlendHeadLookOut
                # def_l_horselink_joint.Footplant
                # def_l_horselink_joint.IKEnabled
                # def_r_horselink_joint.Footplant
                # def_r_horselink_joint.IKEnabled
                # srb.phaseStream
                # X Motion Track
                # Z Motion Track
                # RotY Motion Track
                if name in ("X Motion Track", "Y Motion Track", "Z Motion Track"):
                    k.floats[:, bone_i] *= fac
            # seems to do nothing, apparently not needed
            mi.dtype.has_list = 0
            # if mi.dtype.has_list != 0:
            # 	for limb in k.limb_track_data.limbs:
            # 		for weirdone in limb.keys.list_one:
            # 			weirdone.vec_0.x *= fac
            # 			weirdone.vec_0.y *= fac
            # 			weirdone.vec_0.z *= fac
            # 			weirdone.vec_1.x *= fac
            # 			weirdone.vec_1.y *= fac
            # 			weirdone.vec_1.z *= fac

    @staticmethod
    def get_wsm_name(mi):
        return f"{mi.name}_srb.wsm"

    @property
    def sorted_ms2_bone_names(self):
        return [name for name, bone_index in sorted(self.context.bones_lut.items(), key=lambda item: item[1])]

    def load(self, filepath):
        # clear lut when loading a new file to make sure it is populated afresh
        self.context.bones_lut = {}
        # store file name for later
        self.file = filepath
        self.dir, self.basename = os.path.split(filepath)
        self.path_no_ext = os.path.splitext(self.file)[0]

        with open(filepath, "rb") as stream:
            self.read_fields(stream, self)
            self.eoh = stream.tell()
            # print(self)
            for mani_info in self.mani_infos:
                if hasattr(mani_info, "keys"):
                    mani_info.keys.name = mani_info.name
                    mani_info.keys.compressed.name = mani_info.name

    def update_key_indices(self, mani_info, m_dtype):
        # logging.debug(f"Updating key indices for {m_dtype}")
        MAX_V = self.get_max_v(mani_info)
        k = mani_info.keys
        ms2_bone_names = self.sorted_ms2_bone_names
        m_names = getattr(k, f"{m_dtype}_bones_names")
        # logging.debug(f"ms2_bone_names {len(ms2_bone_names)} = {ms2_bone_names}")
        # logging.debug(f"ms2_bone_indices {len(ms2_bone_names)} = {[self.context.bones_lut[bone_name] for bone_name in ms2_bone_names]}")
        # logging.debug(f"m_names {len(m_names)} = {list(m_names)}")
        try:
            indices = [self.context.bones_lut[bone_name] for bone_name in m_names]
        except KeyError:
            logging.warning(self.context.bones_lut)
            raise
        # map key data index to bone
        getattr(k, f"{m_dtype}_channel_to_bone")[:] = indices
        # logging.debug(f"{m_dtype}_channel_to_bone = {indices}")
        # map bones from selected range in skeleton to index in keyed manis bones
        if indices:
            # get the boundary indices in ms2 bones
            setattr(mani_info, f"{m_dtype}_bone_min", min(indices))
            setattr(mani_info, f"{m_dtype}_bone_max", max(indices))
            key_lut = {name: i for i, name in enumerate(m_names)}
            k.reset_field(f"{m_dtype}_bone_to_channel")
            # logging.debug(f'Len({m_dtype}_bone_to_channel) = {len(getattr(k, f"{m_dtype}_bone_to_channel"))}')
            bone_map_indices = [key_lut.get(name, MAX_V) for name in ms2_bone_names[min(indices): max(indices)+1]]
            # logging.debug(f'min(indices) {min(indices)}')
            # logging.debug(f'max(indices) {max(indices)}')
            # logging.debug(f'bone_map_indices {len(bone_map_indices)} = {bone_map_indices}')
            getattr(k, f"{m_dtype}_bone_to_channel")[:] = bone_map_indices
        else:
            setattr(mani_info, f"{m_dtype}_bone_min", MAX_V)
            setattr(mani_info, f"{m_dtype}_bone_max", 0)
            k.reset_field(f"{m_dtype}_bone_to_channel")

    def save(self, filepath):

        # export supplies a bones_lut, saving has to supply its own
        if not self.context.bones_lut:
            # reconstruct bone indices as used in the ms2
            for mani_info in self.mani_infos:
                for m_dtype in (POS, ORI, SCL):
                    channel_to_bone = getattr(mani_info.keys, f"{m_dtype}_channel_to_bone")
                    m_names = getattr(mani_info.keys, f"{m_dtype}_bones_names")
                    assert len(channel_to_bone) == len(m_names)
                    for i, b in zip(channel_to_bone, m_names):
                        if b in self.context.bones_lut and self.context.bones_lut[b] != i:
                            logging.warning(f"Bone {b} is used with several indices ({i} vs {self.context.bones_lut[b]})")
                        self.context.bones_lut[b] = i

            # ensure lut is fully sampled so that indexing works
            for mani_info in self.mani_infos:
                # maybe check they all have the same target count?
                for i in range(mani_info.target_bone_count):
                    if i not in self.context.bones_lut.values():
                        dummy_name = f"DummyBone{i}"
                        logging.debug(f"Adding {dummy_name}")
                        self.context.bones_lut[dummy_name] = i

        self.mani_count = len(self.mani_infos)
        self.names[:] = [mani.name for mani in self.mani_infos]
        self.header.mani_files_size = self.mani_count * 16
        target_names = set()
        for mani_info in self.mani_infos:
            # logging.debug(f"ManiInfo {mani_info.name} getting names")
            try:
                k = mani_info.keys
            except AttributeError:
                logging.warning(f"ManiInfo {mani_info.name} has no keys")
                raise
            target_names.update(k.pos_bones_names)
            target_names.update(k.ori_bones_names)
            target_names.update(k.scl_bones_names)
            target_names.update(k.floats_names)
        self.header.hash_block_size = len(target_names) * 4
        self.reset_field("name_buffer")
        self.name_buffer.target_names[:] = sorted(target_names)
        self.name_buffer.target_hashes[:] = [djb2(name.lower()) for name in self.name_buffer.target_names]

        for mani_info in self.mani_infos:
            logging.debug(f"Updating {mani_info.name}")
            self.update_key_indices(mani_info, POS)
            self.update_key_indices(mani_info, ORI)
            self.update_key_indices(mani_info, SCL)
        super().save(filepath)

    def get_mani(self, name):
        for mani_info in self.mani_infos:
            if mani_info.name == name:
                return mani_info
        raise AttributeError(f"Name {name} not found")

    @staticmethod
    def get_segment_frame_count(i, frame_count):
        return min(SEGMENT_FRAME_COUNT, frame_count - (i * SEGMENT_FRAME_COUNT))

    def show_keys_by_dtype(self, mani_name, dtype, bone_name, ax: 'matplotlib.axes.Axes'):
        mani_info = self.get_mani(mani_name)
        k = mani_info.keys
        names = getattr(k, f"{dtype}_names")
        assert bone_name in names
        bone_i = names.index(bone_name)
        if dtype == "floats":
            ax.plot(k.floats[:, bone_i], label="floats")
        else:
            if mani_info.dtype.compression:
                self.decompress(mani_info)
            if k.compressed:
                # mark every 32 frame
                for x in range(0, mani_info.frame_count, 32):
                    ax.axvline(x, color=(0, 0, 0, 0.2), linestyle='--', label='',)
            keys = getattr(k, dtype)
            ax.plot(keys[:, bone_i, 0], label='X')
            ax.plot(keys[:, bone_i, 1], label='Y')
            ax.plot(keys[:, bone_i, 2], label='Z')
            if len(keys[0, 0]) > 3:
                ax.plot(keys[:, bone_i, 3], label='Q')
        ax.legend(loc="lower right")

    def decompress(self, mani_info, dump=False):
        if BinStream is None:
            raise ModuleNotFoundError("Install the 'bitarray' module to decompress animations")
        ck = mani_info.keys.compressed
        k = mani_info.keys
        start = time.perf_counter()
        logging.debug(f"Decompressing {mani_info.name} with {len(ck.segments)} segments, {mani_info.frame_count} frames")
        original_compression = mani_info.dtype.compression
        original_has_list = mani_info.dtype.has_list
        mani_info.dtype.compression = 0
        mani_info.dtype.has_list = 0
        k.reset_field("pos_bones")
        k.reset_field("ori_bones")
        assert ck.pos_bone_count == mani_info.pos_bone_count
        assert ck.ori_bone_count == mani_info.ori_bone_count

        frame_offset = 0
        for segment_i, segment in enumerate(ck.segments):
            if dump:
                with open(os.path.join(self.dir, f"{mani_info.name}_{segment_i}.maniskeys"), "wb") as f:
                    f.write(segment.data)
            segment_frames_count = self.get_segment_frame_count(segment_i, mani_info.frame_count)
            segment_pos_bones = k.pos_bones[frame_offset:frame_offset + segment_frames_count]
            segment_ori_bones = k.ori_bones[frame_offset:frame_offset + segment_frames_count]

            context = None
            try:
                context = KeysContext(BinStream(segment.data), segment_frames_count)
                self.read_pos_keys(context, segment_i, mani_info, segment_frames_count, segment_pos_bones)
                self.read_ori_keys(context, segment_i, mani_info, segment_frames_count, segment_ori_bones)
            except Exception as error:
                mani_info.dtype.compression = original_compression
                mani_info.dtype.has_list = original_has_list
                bit_position = context.stream.pos if context is not None else "unknown"
                raise RuntimeError(
                    f"Failed to decode {mani_info.name} segment {segment_i} "
                    f"(frames {frame_offset}-{frame_offset + segment_frames_count}, "
                    f"bit {bit_position}, {len(segment.data)} bytes)"
                ) from error
            frame_offset += segment_frames_count

        loc_min = ck.loc_bounds.mins[ck.loc_bound_indices]
        loc_ext = ck.loc_bounds.scales[ck.loc_bound_indices]
        k.pos_bones *= loc_ext
        k.pos_bones += loc_min
        logging.debug(f"Decompressed {mani_info.name} in {time.perf_counter() - start:.3f} seconds")

    def read_pos_keys(self, context, segment_i, mani_info, segment_frames_count, segment_pos_bones):
        zero_delta = np.zeros(3, dtype=np.float32)
        for bone_i, _bone_name in enumerate(mani_info.keys.pos_bones_names):
            vec, keys_flag = self.read_vec3(context.stream)
            base = np.asarray(vec[:3] * PACK_SCALE, dtype=np.float32)

            if not has_stored_keys(keys_flag):
                segment_pos_bones[:, bone_i] = base
                continue

            raw_keys, stored_frames = context.read_golomb_rice_data(segment_frames_count, keys_flag)
            segment_pos_bones[0, bone_i] = base
            previous_delta = zero_delta.copy()
            current_delta = zero_delta.copy()
            final = base.copy()
            scale = PACK_SCALE

            for frame_i in range(1, segment_frames_count):
                if stored_frames[frame_i]:
                    predicted_delta = np.asarray(
                        np.float32(2.0) * current_delta - previous_delta,
                        dtype=np.float32,
                    )
                    raw_delta = np.asarray(raw_keys[frame_i], dtype=np.float32)
                    predicted_base = clamp_normalized_vector(final + predicted_delta)
                    scaled_delta = np.asarray(raw_delta * scale, dtype=np.float32)
                    final = np.asarray(predicted_base + scaled_delta, dtype=np.float32)
                    previous_delta = current_delta.copy()
                    current_delta = np.asarray(
                        predicted_delta + scaled_delta,
                        dtype=np.float32,
                    )
                else:
                    previous_delta.fill(0.0)
                    current_delta.fill(0.0)
                    scale = PACK_SCALE

                # Native output is saturated while packing to signed-normalized
                # int16. Preserve its range here; exact int16 rounding is not
                # needed for the later location-bounds transform.
                segment_pos_bones[frame_i, bone_i] = clamp_normalized_vector(final)

        logging.debug(f"Segment[{segment_i}] position keys ended at bit {context.stream.pos} (byte {context.stream.pos / 8:.3f})")

    def read_ori_keys(
        self,
        context,
        segment_i,
        mani_info,
        segment_frames_count,
        segment_ori_bones,
    ):
        quantisation_level = mani_info.keys.compressed.quantisation_level
        for bone_i, _bone_name in enumerate(mani_info.keys.ori_bones_names):
            rotation_vector, keys_flag = self.read_vec3(context.stream)
            rotation_vector = np.asarray(
                rotation_vector * ROTATION_VECTOR_SCALE,
                dtype=np.float32,
            )
            base_quat = axis_angle_vector_to_quaternion(rotation_vector)

            if not has_stored_keys(keys_flag):
                segment_ori_bones[:, bone_i] = base_quat
                continue

            raw_keys, stored_frames = context.read_golomb_rice_data(
                segment_frames_count,
                keys_flag,
            )

            # q and -q encode the same orientation. The native decoder starts
            # relative updates from the representative with non-negative W.
            current_quat = -base_quat if base_quat[3] < 0.0 else base_quat.copy()
            segment_ori_bones[0, bone_i] = current_quat

            accumulated_xyz = np.zeros(3, dtype=np.float32)
            scale = PACK_SCALE
            for frame_i in range(1, segment_frames_count):
                if stored_frames[frame_i]:
                    raw_delta = np.asarray(raw_keys[frame_i], dtype=np.float32)
                    relative_xyz = np.asarray(
                        accumulated_xyz + raw_delta * scale,
                        dtype=np.float32,
                    )

                    # Relative keys always omit W. The decoder reconstructs the
                    # non-negative root; this is fixed-W, not smallest-three.
                    relative_quat = reconstruct_relative_quaternion(relative_xyz)
                    candidate = normalize_quaternion_or_identity(
                        multiply_quaternions(current_quat, relative_quat)
                    )

                    accumulated_xyz = np.asarray(
                        np.clip(relative_xyz, -1.0, 1.0),
                        dtype=np.float32,
                    )
                    state_norm = np.float32(
                        np.clip(np.linalg.norm(accumulated_xyz), 0.0, 1.0)
                    )
                    scale = get_rotation_pack_scale(
                        quantisation_level,
                        state_norm,
                    )
                    current_quat = candidate
                else:
                    # Native held frames clear both pieces of relative state.
                    accumulated_xyz.fill(0.0)
                    scale = PACK_SCALE

                segment_ori_bones[frame_i, bone_i] = current_quat

        logging.debug(f"Segment[{segment_i}] rotation keys ended at bit {context.stream.pos} (byte {context.stream.pos / 8:.3f})")

    def read_vec3(self, stream: BinStream) -> tuple[np.ndarray, StoreKeys]:
        """Read a zigzag-coded 15/15/15 base triplet and its X/Y/Z key mask."""
        if self.context.version > 259:
            encoded = [stream.read_uint(COMPONENT_BITS) for _ in range(3)]
        else:
            encoded = [stream.read_uint_reversed(COMPONENT_BITS) for _ in range(3)]

        vec = np.asarray(
            stream.decode_zigzag(*encoded, 0),
            dtype=np.float32,
        )
        keys_flag = StoreKeys.from_value(stream.read_uint(3))
        return vec, keys_flag


if __name__ == "__main__":
    from utils.logs import logging_setup
    logging_setup("manis")
    for k in (0, 1, 4, 5, 6, 8, 9, 14, 32, 34, 36, 37, 38, 64, 66, 68, 69, 70, 82, 48, 112, 113, 114):
        print(ManisDtype.from_value(k))
    manis = ManisFile()
