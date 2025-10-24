from generated.formats.manis.imports import name_type_map
import logging
import math
import os
import time
from copy import copy

import numpy as np

from modules.formats.shared import djb2

np.seterr(all='warn')
# np.seterr(all='print')
np.set_printoptions(precision=4, suppress=True)

from ovl_util.logs import logging_setup
from generated.io import IoFile
from generated.formats.manis.versions import get_game, set_game
from generated.formats.manis.bitfields.StoreKeys import StoreKeys
from generated.formats.manis.structs.InfoHeader import InfoHeader
from generated.formats.manis.bitfields.ManisDtype import ManisDtype

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
            assert len(d) == size, f"Reached end of chunk reading {size} bits at bit {self.pos}, byte {self.pos / 8}, got {len(d)} bits"
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

        @staticmethod
        def interpret_as_shift(size: int, flag: int):
            return flag * ((1 << size) - 1)

        def read_bit_size_flag(self, max_size: int):
            for rel_key_size in range(max_size):
                new_bit = self.read_uint(1)
                if not new_bit:
                    return rel_key_size
            return -1

        @staticmethod
        def decode_zigzag(*args):
            # use zigzag encoding
            return [-(x + 1 >> 1) if x & 1 else x >> 1 for x in args]

        def find_all(self, bits):
            for match_offset in self.data.itersearch(bits):
                yield match_offset

except:
    BinStream = None
    logging.warning(f"bitarray module is not installed")


POS = "pos"
ORI = "ori"
SCL = "scl"
FLO = "float"
EUL = "euler"
root_name = "def_c_root_joint"
srb_name = "srb"


class KeysContext:
    def __init__(self, stream, segment_frames_count):
        self.stream = stream
        # this is a jump to the end of the compressed keys
        context_offset = stream.read_uint_reversed(16) * 8
        logging.debug(f"context at bit {context_offset}")
        self.stream.seek(context_offset)
        if segment_frames_count == 1:
            # JWE2 carcharo standtorun - points to end of stream
            if self.stream.data.nbytes == context_offset:
                logging.debug(f"Stream has no context")
            else:
                # stream can have 00 00 at context_offset for a segment with 1 frame = no relative keys
                empty = self.stream.read_uint(16)
                assert empty == 0, "Stream with no relative keys must have 00 00 context"
            self.do_increment = self.runs_remaining = self.init_k_a = self.init_k_b = 0
        else:
            self.do_increment = self.stream.read_uint(1)
            self.runs_remaining = self.stream.read_uint(16)
            self.init_k_a = self.stream.read_uint_reversed(4)
            self.init_k_b = self.stream.read_uint_reversed(4)
            if not self.do_increment:
                self.init_k_a, self.init_k_b = self.init_k_b, self.init_k_a
            logging.debug(self)
            self.do_increment = not self.do_increment
            self.begun = True
            self.i_in_run = 0
        self.golomb_rice_offset = stream.pos
        # self.keys_offset = 16
        # seek to start of base keys
        stream.seek(16)

    def read_golomb_rice_data(self, segment_frames_count, keys_flag):
        raw_keys_storage = np.zeros((52, 3), dtype=np.float32)
        frame_map = np.zeros(32, dtype=np.uint32)
        # logging.info(f"golomb_rice at bit {self.stream.pos}")
        keyframe_count = 0

        keys_offset = self.stream.pos
        self.stream.seek(self.golomb_rice_offset)
        for frame_i in range(1, segment_frames_count):
            if self.i_in_run == 0:
                assert self.runs_remaining != 0
                self.runs_remaining -= 1
                self.do_increment = not self.do_increment
                init_k = self.init_k_a if self.do_increment else self.init_k_b
                assert init_k < 32
                # logging.info(f"do_increment {do_increment} init_k {init_k} at {self.stream.pos}")
                k_size = self.stream.read_bit_size_flag(32 - init_k)
                k_flag = 1 << (init_k & 0x1f)
                k_flag_out = self.stream.interpret_as_shift(k_size, k_flag)
                # logging.info(
                # 	f"pos before key {self.stream.pos}, k_flag_out {k_flag_out}, init_k bare {k_size}")
                k_key = self.stream.read_uint_reversed(k_size + init_k)
                assert k_size + init_k < 32
                self.i_in_run = k_key + k_flag_out
            # logging.info(
            # 	f"golomb_rice[{frame_i}] total init_k {init_k + k_size} key {k_key} k_flag_out {k_flag_out} i {i_in_run}")
            # logging.info(f"pos after read {self.stream.pos}")
            self.i_in_run -= 1
            if self.do_increment:
                frame_map[keyframe_count] = frame_i
                keyframe_count += 1
        self.golomb_rice_offset = self.stream.pos
        self.stream.seek(keys_offset)
        for channel_i, is_active in enumerate((keys_flag.x, keys_flag.y, keys_flag.z)):
            if is_active:
                # logging.info(f"rel_keys[{channel_i}] at bit {context.stream.pos}")
                # define the minimal key size for this channel
                ch_key_size = self.stream.read_uint_reversed(4)
                ch_key_size_masked = ch_key_size & 31
                assert ch_key_size <= 32
                # logging.info(f"channel[{channel_i}] base_size {ch_key_size} at bit {context.stream.pos}")
                for trg_frame_i in frame_map[:keyframe_count]:
                    rel_key_flag = 1 << ch_key_size_masked | 1 >> (32 - ch_key_size_masked)
                    # rel_key_size = context.stream.read_bit_size_flag(15 - ch_key_size_masked)
                    rel_key_size = self.stream.read_bit_size_flag(32)
                    # todo this may have to be shifted only with the corresponding clamp applied
                    rel_key_base = self.stream.interpret_as_shift(rel_key_size, rel_key_flag)
                    ch_rel_key_size = ch_key_size + rel_key_size
                    # clamp key size to 0-15 bits
                    ch_rel_key_size = min(ch_rel_key_size, 15)
                    # ensure the final key size is valid
                    assert ch_rel_key_size <= 32
                    # logging.info(f"ch_rel_key_size {ch_rel_key_size}")
                    # read the key, if it has a size
                    if ch_rel_key_size:
                        ch_rel_key = self.stream.read_uint_reversed(ch_rel_key_size)
                    else:
                        ch_rel_key = 0
                    # logging.info(f"key = {ch_rel_key}")
                    rel_key_masked = (rel_key_base + ch_rel_key) & 0xffff
                    raw_keys_storage[trg_frame_i, channel_i] = self.stream.decode_zigzag(rel_key_masked)[0]
        return raw_keys_storage, frame_map

    def __repr__(self):
        return f"Context: do_increment {self.do_increment}, runs_remaining {self.runs_remaining}, init_k_a {self.init_k_a}, init_k_b {self.init_k_b}"


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
        for model_info in self.mani_infos:
            if model_info.name == new_name:
                return True
        return False

    def rename_file(self, old, new):
        logging.info(f"Renaming .mani in {self.name}")
        for model_info in self.mani_infos:
            if model_info.name == old:
                model_info.name = new

    def remove(self, mani_names):
        logging.info(f"Removing {len(mani_names)} .mani files in {self.name}")
        for model_info in reversed(self.mani_infos):
            if model_info.name in mani_names:
                self.mani_infos.remove(model_info)

    def duplicate(self, mani_names):
        logging.info(f"Duplicating {len(mani_names)} .mani files in {self.name}")
        for model_info in reversed(self.mani_infos):
            if model_info.name in mani_names:
                model_info_copy = copy(model_info)
                # add as many suffixes as needed to make new_name unique
                self.make_name_unique(model_info_copy)
                self.mani_infos.append(model_info_copy)
        self.mani_infos.sort(key=lambda model_info: model_info.name)

    def make_name_unique(self, model_info_copy):
        new_name = model_info_copy.name
        while self.name_used(new_name):
            new_name = f"{new_name}_copy"
        model_info_copy.name = new_name

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
        bone_name = "srb"
        wsm_name = f"{mi.name}_{bone_name}.wsm"
        return wsm_name

    @property
    def sorted_ms2_bone_names(self):
        return [n for n, i in sorted(self.context.bones_lut.items(), key=lambda kv: kv[1])]

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
                # print(mi.keys.name)
                # if mi.root_pos_bone != 255:
                # 	print(mi.root_pos_bone, mi.keys.pos_bones_names[mi.root_pos_bone])
                # if mi.root_ori_bone != 255:
                # 	print(mi.root_ori_bone, mi.keys.ori_bones_names[mi.root_ori_bone])

    def update_key_indices(self, mani_info, m_dtype):
        # logging.debug(f"Updating key indices for {m_dtype}")
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
            bone_map_indices = [key_lut.get(name, 255) for name in ms2_bone_names[min(indices): max(indices)+1]]
            # logging.debug(f'min(indices) {min(indices)}')
            # logging.debug(f'max(indices) {max(indices)}')
            # logging.debug(f'bone_map_indices {len(bone_map_indices)} = {bone_map_indices}')
            getattr(k, f"{m_dtype}_bone_to_channel")[:] = bone_map_indices
        else:
            setattr(mani_info, f"{m_dtype}_bone_min", 255)
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
            except:
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

    def iter_compressed_manis(self):
        for mani_info in self.mani_infos:
            if hasattr(mani_info, "keys"):
                if mani_info.dtype.compression and hasattr(mani_info.keys.compressed, "segments"):
                    yield mani_info

    def iter_uncompressed_manis(self):
        for mani_info in self.mani_infos:
            if hasattr(mani_info, "keys"):
                if not mani_info.dtype.compression:
                    yield mani_info

    def iter_compressed_keys(self):
        for mani_info in self.iter_compressed_manis():
            # logging.info(mani_info.keys.compressed)
            for i, mb in enumerate(mani_info.keys.compressed.segments):
                yield mani_info, i, mb

    def dump_keys(self):
        for mani_info, i, mb in self.iter_compressed_keys():
            with open(os.path.join(self.dir, f"{mani_info.name}_{i}.maniskeys"), "wb") as f:
                f.write(mb.data)

    @staticmethod
    def get_segment_frame_count(i, frame_count):
        # get from chunk index
        return min(32, frame_count - (i * 32))

    def log_loc_keys(self):
        for mani_info in self.iter_uncompressed_manis():
            # logging.info(mani_info)
            for pos_index, pos_name in enumerate(mani_info.keys.pos_bones_names):
                v = mani_info.keys.pos_bones[0][pos_index]
                x, y, z = v.x, v.y, v.z
                logging.info(f"unc {pos_index} {pos_name} {(x, y, z)}")
            break

    def log_rot_keys(self):
        for mani_info in self.iter_uncompressed_manis():
            # logging.info(mani_info)
            for ori_index, ori_name in enumerate(mani_info.keys.ori_bones_names):
                v = mani_info.keys.ori_bones[0][ori_index]
                x, y, z, w = v.x, v.y, v.z, v.w
                # if "def_c_hips_joint" == ori_name:
                #     logging.info(f"{ori_index} {ori_name} {(x, y, z, w)}")

    def parse_keys(self, target=None, dump=False):
        for mani_info in self.iter_compressed_manis():
            if target and mani_info.name != target:
                continue
            # acro debug keys
            pkg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
            dump_path = os.path.join(pkg_dir, "dumps", f"{mani_info.name}_keys.txt")
            if os.path.isfile(dump_path):
                logging.info(f"Found reference keys for {mani_info.name}")
                keys = [int(line.strip(), 0) for line in open(dump_path, "r")]
                keys_iter = iter(keys)
            # logging.info(mani_info)
            # logging.info(mani_info.keys.compressed)
            try:
                self.decompress(mani_info, dump=dump)
            except:
                logging.exception(f"Decompressing {mani_info.name} failed")

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
                ck = k.compressed
                if not hasattr(ck, dtype):
                    self.decompress(mani_info)
                keys = getattr(ck, dtype)
                # mark every 32 frame
                ax.vlines(range(0, len(keys[:, bone_i, 0]), 32), -1, 1, colors=(0, 0, 0, 0.2), linestyles='--', label='',)
            else:
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
        start = time.time()
        logging.debug(
            f"Decompressing {mani_info.name} with {len(ck.segments)} segments, {mani_info.frame_count} frames")
        ck.pos_bones = np.empty((mani_info.frame_count, mani_info.pos_bone_count, 3), np.float32)
        ck.ori_bones = np.empty((mani_info.frame_count, mani_info.ori_bone_count, 4), np.float32)
        assert ck.pos_bone_count == mani_info.pos_bone_count
        assert ck.ori_bone_count == mani_info.ori_bone_count
        frame_offset = 0
        for segment_i, segment in enumerate(ck.segments):
            # dump compressed segment data if needed
            if dump:
                with open(os.path.join(self.dir, f"{mani_info.name}_{segment_i}.maniskeys"), "wb") as f:
                    f.write(segment.data)
            segment_frames_count = self.get_segment_frame_count(segment_i, mani_info.frame_count)
            # create views into the complete data for this segment
            segment_pos_bones = ck.pos_bones[frame_offset:frame_offset + segment_frames_count]
            segment_ori_bones = ck.ori_bones[frame_offset:frame_offset + segment_frames_count]
            try:
                context = KeysContext(BinStream(segment.data), segment_frames_count)
                self.read_pos_keys(context, segment_i, mani_info, segment_frames_count, segment_pos_bones)
                self.read_ori_keys(context, segment_i, mani_info, segment_frames_count, segment_ori_bones)
            except:
                logging.exception(f"Reading Segment[{segment_i}] (frames {frame_offset}-{frame_offset+segment_frames_count}) failed at bit {context.stream.pos}, byte {context.stream.pos / 8}, size {len(segment.data)} bytes")
            frame_offset += segment_frames_count
        loc_min = ck.loc_bounds.mins[ck.loc_bound_indices]
        loc_ext = ck.loc_bounds.scales[ck.loc_bound_indices]
        ck.pos_bones *= loc_ext
        ck.pos_bones += loc_min
        logging.debug(
            f"Decompressed {mani_info.name} in {time.time() - start:.3f} seconds")

    def read_pos_keys(self, context, segment_i, mani_info, segment_frames_count, segment_pos_bones):
        identity = np.zeros(3, np.float32)
        scale = self.get_pack_scale(mani_info)
        for pos_index, pos_name in enumerate(mani_info.keys.pos_bones_names):
            # defines basic loc value; not byte aligned
            vec = self.read_vec3(context.stream)[:3]
            vec *= scale
            # the scale per bone is always norm = 0 in acro_run
            scale_pack = self.get_pack_scale(mani_info)
            # which channels are keyframed
            keys_flag = context.stream.read_uint(3)
            keys_flag = StoreKeys.from_value(keys_flag)
            if keys_flag.x or keys_flag.y or keys_flag.z:
                raw_keys_storage, frame_map = context.read_golomb_rice_data(segment_frames_count, keys_flag)
                if segment_frames_count > 1:
                    frame_inc = 0
                    # set base keyframe
                    segment_pos_bones[0, pos_index] = vec
                    # set other keyframes
                    last_key_a = identity
                    last_key_b = identity
                    final = vec.copy()
                    for out_frame_i in range(1, segment_frames_count):
                        trg_frame_i = frame_map[frame_inc]
                        out = raw_keys_storage[out_frame_i]
                        # todo - scale or sth before for JWE2 dev acro, only single channels, so probably fairly early
                        #  motionextracted.manisetf96acca0.manis acrocanthosaurus@jumpattackdefendthrowright, segment[2], root, Y
                        #  motionextracted.maniset85c65403 acrocanthosaurus@walk, segment[0], def_horselink_joint_IKBlend.L, Z; segment[1] is fine
                        #  maybe create a dedicated copy that includes just that bone?
                        last_key_delta = 2 * last_key_b - last_key_a
                        if out_frame_i == trg_frame_i:
                            frame_inc += 1
                            # a key is stored for this frame
                            # instead of scale_pack, this scale is hard-coded to the corresponding float of 1 / 16383
                            final = final + last_key_delta + out * 6.103888e-05
                            last_key_a = last_key_b.copy()
                            # this scale uses the calculated scale
                            last_key_b = last_key_delta + out * scale_pack
                        else:
                            # hold key from previous frame
                            # print(pos_index, segment_i* 32 + out_frame_i)
                            final = segment_pos_bones[out_frame_i-1, pos_index]
                            last_key_a = identity
                            last_key_b = identity
                            # update scale_pack here, todo check if / what norm is used with conditional breakpoint
                            # apparently also norm = 0 in acro_run, but too many to properly verify that for successive bones
                            scale_pack = self.get_pack_scale(mani_info)
                        segment_pos_bones[out_frame_i, pos_index] = final
            else:
                # set all keyframes
                segment_pos_bones[:, pos_index] = vec
        logging.debug(f"Segment[{segment_i}] loc finished at bit {context.stream.pos}, byte {context.stream.pos / 8}")

    @staticmethod
    def printm(v):
        """print in order of memory register"""
        print(list(reversed(v)))

    def read_ori_keys(self, context, segment_i, mani_info, segment_frames_count, segment_ori_bones):
        q_scale = 2 * math.pi  # 6.283185
        epsilon = 1.1920929E-7  # 1 / 8388608 (=2**23)
        zeros = np.zeros(4, dtype=np.float32)
        identity = zeros.copy()
        identity[3] = 1.0
        scale = self.get_pack_scale(mani_info)
        for ori_index, ori_name in enumerate(mani_info.keys.ori_bones_names):
            # logging.info(context)
            # defines basic rot values
            # logging.info(f"ori[{ori_index}] {ori_name} at bit {context.stream.pos}")
            vec = self.read_vec3(context.stream)
            scale_pack = float(scale)
            # vec *= scale_pack * q_scale
            vec *= scale * q_scale
            norm = np.linalg.norm(vec)
            # logging.info(f"{ori_index} {ori_name} {vec} {norm}")
            if norm < epsilon:
                quat = identity.copy()
            else:
                q, scale_fac = get_quat_scale_fac(norm * 0.5)
                quat = vec / norm
                quat *= scale_fac
                quat[3] = q

            # which channels are keyframed
            keys_flag = context.stream.read_uint(3)
            keys_flag = StoreKeys.from_value(keys_flag)
            if keys_flag.x or keys_flag.y or keys_flag.z:
                raw_keys_storage, frame_map = context.read_golomb_rice_data(segment_frames_count, keys_flag)
                # logging.info(f"key {i} = {rel_key_masked}")
                if segment_frames_count > 1:
                    frame_inc = 0
                    out = np.zeros(4, float)
                    # sign flipping happens before setting quat itself but for cleaner output in the graphs
                    quat = quat * -1 if quat[3] < 0 else quat
                    # set base keyframe
                    # logging.info(f"BASE 0: {quat}, {ori_index}")
                    segment_ori_bones[0, ori_index] = quat
                    quat_pos = quat
                    last_key_a = zeros.copy()
                    # set other keyframes
                    for out_frame_i in range(1, segment_frames_count):
                        trg_frame_i = frame_map[frame_inc]

                        out[:3] = raw_keys_storage[out_frame_i]
                        out[3] = 0.0
                        # todo figure out logic for scale
                        #  animationmotionextractedlocomotion.maniset535f4cdb, mandrill_male@runbase, bone 41 breaks after frame 2
                        #  https://github.com/OpenNaja/cobra-tools/issues/385
                        # scale fac (actually dynamic)
                        # 6.10389e-005 6.10389e-005 6.10389e-005 6.10389e-005
                        # 0.000103384 0.000103384 0.000103384 0.000103384
                        # 0.00015692 0.00015692 0.00015692 0.00015692
                        # 0.000169376 0.000169376 0.000169376 0.000169376
                        # 0.000182325 0.000182325 0.000182325 0.000182325

                        scaled_rel_key = out * scale_pack
                        # these are ok
                        out = scaled_rel_key + last_key_a
                        q = math.sqrt(max(0.0, 1.0 - np.sum(np.square(out))))
                        # q stays 0.0
                        rel_scaled = out.copy()
                        rel_scaled_q = out.copy()
                        rel_scaled_q[3] = q

                        rel_inter = out.copy()
                        rel_inter[0] = (quat_pos[0] * q + quat_pos[1] * rel_scaled_q[2]) - (quat_pos[2] * rel_scaled_q[1] - quat_pos[3] * rel_scaled_q[0])
                        rel_inter[1] = quat_pos[2] * q + quat_pos[3] * rel_scaled_q[2] + (quat_pos[0] * rel_scaled_q[1] - quat_pos[1] * rel_scaled_q[0])
                        rel_inter[2] = (q * quat_pos[3] - rel_scaled_q[2] * quat_pos[2]) - (rel_scaled_q[1] * quat_pos[1] + rel_scaled_q[0] * quat_pos[0])
                        rel_inter[3] = (q * quat_pos[1] - rel_scaled_q[2] * quat_pos[0]) + rel_scaled_q[1] * quat_pos[3] + rel_scaled_q[0] * quat_pos[2]
                        norm = np.linalg.norm(rel_inter)
                        # scaled_inter is set to identity if norm == 0.0
                        if norm == 0.0:
                            scaled_inter = identity.copy()
                        else:
                            # normalize and swizzle the quat
                            scaled_inter = rel_inter[[0, 3, 1, 2]] / norm
                        # if 0 == ori_index:
                        #     # self.printm(rel_inter)
                        #     # print(norm)
                        #     self.printm(scaled_inter)

                        # xmm12 0 0 -0.000366233 0
                        # probably not clipped to 0.0, but -1.0
                        rel_scaled_clamped_copy = np.clip(rel_scaled, -1.0, 1.0)
                        # if 0 == ori_index:
                        #     # [0.0, 0.0, -0.0003662333, 0.0]
                        #     self.printm(rel_scaled_clamped_copy)
                        # dbg 0 0 1.34127e-007 0.000366233  # only last coord is set to sqrt
                        norm = np.linalg.norm(rel_scaled_clamped_copy)
                        norm = np.clip(norm, 0.0, 1.0)
                        scale_pack = self.get_pack_scale(mani_info, norm)
                        # not sure about the cond here
                        # print(quant_fac_clamped)
                        # if 0.0 <= norm <= 0.5:
                        #     quant_fac_picked = quant_fac_clamped
                        # else:
                        #     quant_fac_picked = quant_fac_clamped
                        # quant_fac_switched[0] = (float)(quant_fac_clamped[0] & norm_is_0_05);
                        # quant_fac_switched[1] = 0.0;
                        # quant_fac_switched[2] = 0.0;
                        # quant_fac_switched[3] = (float)quant_fac_clamped[3];
                        # vec4f_16383_b[0] = (float)(~norm_is_0_05 & 0x467ffc00);
                        # vec4f_16383_b[1] = 16383.0;
                        # vec4f_16383_b[2] = 16383.0;
                        # vec4f_16383_b[3] = 16383.0;
                        # quant_fac_picked = (float[4])((undefined[16])quant_fac_switched & (undefined[16])0xffffffffffffffff | (undefined[16]) vec4f_16383_b);
                        # scale_rel._0_8_ = CONCAT44(scale_fac / quant_fac_picked[0], quant_fac_picked[0]);
                        # scale_rel[2] = (float)quant_fac_picked[1];
                        # scale_rel[3] = 0.0;

                        # todo check if this is used for more than the isFinite sanity check
                        # todo do sth with quant_fac_picked
                        # todo update scale_pack when needed

                        do_increment = out_frame_i == trg_frame_i
                        next_key_offset = 0 if do_increment else 4
                        which_key_flag = True if next_key_offset else False
                        # last key_a derives from rel_scaled
                        last_key_a = zeros.copy() if which_key_flag else rel_scaled_clamped_copy.copy()

                        if out_frame_i == trg_frame_i:
                            frame_inc += 1
                            final_inter = scaled_inter
                            # use scaled_inter_vec_copy
                        else:
                            # todo another round of clamping
                            # transfer signs from sign_source, store on ptr_to_final?
                            # use recon quat instead
                            final_inter = quat_pos

                        # self.printm(final_inter)
                        # quat aka recon_quat is set to last key of curve for the next loop, todo verify
                        quat_pos = final_inter
                        # logging.info(f"INTER {out_frame_i}: {final_inter}, {ori_index}")
                        segment_ori_bones[out_frame_i, ori_index, ] = final_inter
                    # break
            else:
                # set all keyframes
                segment_ori_bones[:, ori_index] = quat
        logging.debug(f"Segment[{segment_i}] rot finished at bit {context.stream.pos}, byte {context.stream.pos / 8}")

    def get_pack_scale(self, mani_info, norm=0.000000000000000000000001):
        # the default initial scale seems to be for loc and rot
        # 1 / 16383 = 6.103888e-05
        # apparently starting out with norm=0
        # 0.00036623328924179077
        # print(norm)
        # xmm1 0 0 0 2730.5  # scale_f = 1 / norm
        # quantisation_level 420
        # just set non-zero to avoid RuntimeWarning
        norm = max(norm, 0.000000000000000000000001)
        quant_fac = mani_info.keys.compressed.quantisation_level / norm
        # quant_fac in xmm3 0 0 0 1.14681e+006
        # quant_fac = 1146810.0
        quant_fac_clamped = np.clip(quant_fac, 128.0, 16383.0)
        # update the packed scale
        return 1 / quant_fac_clamped

    def read_vec3(self, f: BinStream):
        if self.context.version > 259:
            # current PZ, JWE2
            x = f.read_uint(15)
            y = f.read_uint(15)
            z = f.read_uint(15)
        else:
            # PC, JWE1, old PZ have the order reversed
            x = f.read_uint_reversed(15)
            y = f.read_uint_reversed(15)
            z = f.read_uint_reversed(15)
        vec = np.zeros(4, dtype=np.float32)
        vec[:] = f.decode_zigzag(x, y, z, 0)
        return vec


def get_quat_scale_fac(norm_half_abs: float):
    epsilon = 1.1920929E-7
    cos = np.cos(norm_half_abs)
    sin = np.sin(norm_half_abs)
    # wrap to 2pi range, then check whether to apply flips
    octant = int(norm_half_abs % (2*np.pi) / np.pi * 4 - epsilon)
    if 4 < octant < 7:
        sin = -sin
        cos = -cos
    return cos, sin


if __name__ == "__main__":
    logging_setup("mani")
    for k in (0, 1, 4, 5, 6, 8, 9, 14, 32, 34, 36, 37, 38, 64, 66, 68, 69, 70, 82, 48, 112, 113, 114):
        print(ManisDtype.from_value(k))
    mani = ManisFile()
    # WH
    # mani.load("C:/Users/arnfi/Desktop/animation.manisetb22bfc73.manis")  # first is uncompressed
    # mani.load("C:/Users/arnfi/Desktop/animation.maniset273472b1.manis")
