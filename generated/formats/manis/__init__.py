from generated.formats.manis.imports import name_type_map
import contextlib
import logging
import math
import struct
import os
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
from generated.formats.manis.compounds.InfoHeader import InfoHeader
from generated.formats.manis.bitfields.ManisDtype import ManisDtype

try:
    import bitarray
    import bitarray.util
except:
    bitarray = None
    logging.warning(f"bitarray module is not installed")

POS = "pos"
ORI = "ori"
SCL = "scl"
FLO = "float"
EUL = "euler"
root_name = "def_c_root_joint"
srb_name = "srb"


class BinStream:
    def __init__(self, val):
        self.data = bitarray.bitarray(endian='little')
        self.data.frombytes(val)
        self.pos = 0

    def seek(self, pos):
        self.pos = pos

    def read(self, size):
        d = self.data[self.pos: self.pos + size]
        assert len(d) == size, f"Reached end of chunk reading {size} bits at bit {self.pos}, byte {self.pos/8}, got {len(d)} bits"
        self.pos += size
        return d

    def read_int(self, size):
        bits = self.read(size)
        return bitarray.util.ba2int(bits, signed=True)

    def read_uint(self, size):
        bits = self.read(size)
        return bitarray.util.ba2int(bits, signed=False)

    def read_uint_reversed(self, size):
        out = 0
        for _ in range(size):
            new_bit = self.read_uint(1)
            out = new_bit | (out * 2)
        return out

    def interpret_as_shift(self, size, flag):
        out = 0
        for _ in range(size):
            out += flag
            flag *= 2
        return out

    def read_bit_size_flag(self, max_size):
        for rel_key_size in range(max_size):
            new_bit = self.read_uint(1)
            if not new_bit:
                return rel_key_size
        return -1

    def find_all(self, bits):
        for match_offset in self.data.itersearch(bits):
            # logging.info(match)
            yield match_offset


class KeysContext:
    def __init__(self, stream, wavelet_byte_offset, segment_frames_count):
        self.stream = stream
        logging.debug(f"wavelet_byte_offset {wavelet_byte_offset}")
        self.stream.seek(wavelet_byte_offset * 8)
        if segment_frames_count == 1:
            # JWE2 carcharo standtorun - points to end of stream
            if self.stream.data.nbytes == wavelet_byte_offset:
                logging.debug(f"Stream has no context")
            else:
                # stream can have 00 00 at wavelet_byte_offset for a segment with 1 frame = no relative keys
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

    def read_wavelet_table(self, frame_map, segment_frames_count):
        # logging.info(f"wavelets at bit {self.stream.pos}")
        new_wavelets_offset = 0
        for wave_frame_i in range(1, segment_frames_count):
            if self.i_in_run == 0:
                assert self.runs_remaining != 0
                self.runs_remaining -= 1
                self.do_increment = not self.do_increment
                init_k = self.init_k_a if self.do_increment else self.init_k_b
                assert init_k < 32
                # run 0: init_k_a = 2
                # run 1: init_k_b = 4
                # logging.info(f"do_increment {do_increment} init_k {init_k} at {self.stream.pos}")
                k_size = self.stream.read_bit_size_flag(32 - init_k)
                k_flag = 1 << (init_k & 0x1f)
                k_flag_out = self.stream.interpret_as_shift(k_size, k_flag)
                # logging.info(
                # 	f"pos before key {self.stream.pos}, k_flag_out {k_flag_out}, initk bare {k_size}")
                k_key = self.stream.read_uint_reversed(k_size + init_k)
                assert k_size + init_k < 32
                self.i_in_run = k_key + k_flag_out
            # logging.info(
            # 	f"wavelet_frame[{wave_frame_i}] total init_k {init_k + k_size} key {k_key} k_flag_out {k_flag_out} i {i_in_run}")
            # logging.info(f"pos after read {self.stream.pos}")
            self.i_in_run -= 1
            if self.do_increment:
                frame_map[new_wavelets_offset] = wave_frame_i
                new_wavelets_offset += 1

        # logging.info(frame_map)
        # logging.info(f"wavelets finished at bit {self.stream.pos}, byte {self.stream.pos / 8}, out_count {new_wavelets_offset}")
        return new_wavelets_offset
    
    def __repr__(self):
        return f"Context: do_increment {self.do_increment}, runs_remaining {self.runs_remaining}, init_k_a {self.init_k_a}, init_k_b {self.init_k_b}"


def f_as_i(f):
    return np.int32(struct.unpack('<i', struct.pack('<f', f))[0])


def i_as_f(f):
    return np.float32(struct.unpack('<f', struct.pack('<i', f))[0])


@contextlib.contextmanager
def as_int(f):
    i = f_as_i(f)
    yield i
    return i_as_f(i)


def get_quat_scale_fac(norm_half_abs):
    # pointless, as norm is already squared
    # norm_half_abs = abs(norm_half_abs)
    # logging.info(f"half_norm {norm_half_abs}")
    # fVar3 = norm_half_abs * 0.6366197 + 8388608.0
    # masked_8388609 = f_as_i(8388609.0) & f_as_i(fVar3)
    # matches_8388609 = -int(i_as_f(masked_8388609) == 8388609.0)
    # logging.info(f"matches_8388609 {matches_8388609}")
    # fVar4 = fVar3 - 8388608.0
    # logging.info(f"fVar4 {fVar4}")
    # uVar7 = 0 & -(i_as_f(f_as_i(fVar3) & f_as_i(8388610.0)) == 8388610.0)
    # fVar4 = ((norm_half_abs - fVar4 * 1.570313) - fVar4 * 0.0004837513 - fVar4 * 7.54979e-08)# ^ (0 & uVar8)
    # fVar4_squared = fVar4 * fVar4
    # fVar5 = (((0.000024433157 * fVar4_squared + -0.001388732) * fVar4_squared + 0.04166665) * fVar4_squared - 0.5) * fVar4_squared + 1.0
    # fVar4 = ((fVar4_squared * -0.000195153 + 0.008332161) * fVar4_squared + -0.1666666) * fVar4_squared * fVar4 + fVar4
    # scale = (f_as_i(fVar5) & matches_8388609 | f_as_i(fVar4) & ~matches_8388609) ^ uVar7
    # res = np.array(1.0, dtype=np.float32) & np.array(-1, dtype=np.int32)
    # print(res)
    # fVar6 = abs(norm_half_abs)
    # fVar3 = fVar6 * 0.6366197 + 8388608.0
    # uVar4 = f_as_i(8388609.0) & f_as_i(fVar3)
    # uVar8 = -int(i_as_f(uVar4) == 8388609.0)
    # fVar4 = fVar3 - 8388608.0
    # uVar6 = 0.0
    # uVar7 = (uint)uVar6 & -(uint)((float)((uint)fVar3 & f_as_i(8388610.0)) == 8388610.0)
    # uVar9 = 0.000024433157
    # xmm0 = np.float32(1.0)
    # # xmm0 = 2.0
    # print(xmm0, type(xmm0))
    # raise AttributeError

    xmm2 = np.float32(8388608.0)  # 00 00 00 4B
    xmm0 = np.float32(8388609.0)  # 01 00 00 4B
    xmm1 = np.float32(8388610.0)  # 02 00 00 4B
    # store new norm at ptr (used to have old norm)
    xmm3 = xmm1  # copy 8388610f to xmm3
    # store 1.0 vec4f at ptr (not sure what it does)
    xmm7 = xmm0  # copy 8388609f
    # store 0 0 0 0 0 16383 6.10389e-005 16383 at ptr (not sure why)
    xmm8 = np.float32(norm_half_abs)  # move halfnorm to xmm8 from ptr
    xmm6 = xmm8  # copy halfnorm from xmm8 to xmm6
    xmm6 = np.abs(xmm6)  # take abs of xmm6 (copy of halfnorm)
    xmm4 = xmm6  # copy abs halfnorm to xmm4
    xmm4 *= np.float32(0.6366197)  # halfnorm
    xmm4 += xmm2  # halfnorm + 8388608f
    xmm3 = i_as_f(f_as_i(xmm3) & f_as_i(xmm4))  # mask xmm3 (...10f) with xmm4 (halfnorm+...8f)
    xmm7 = i_as_f(f_as_i(xmm7) & f_as_i(xmm4))  # mask xmm7 (...9f) with xmm4 (halfnorm+...8f)
    xmm3 = xmm3 == xmm1  # compare equality of masked and ..10f -> xmm3 = 0
    xmm7 = xmm7 == xmm0  # compare equality of masked and ..9f -> xmm7 = -1 or 0
    # xmm3 = i_as_f(-1 if xmm3 else 0)
    # xmm7 = i_as_f(-1 if xmm7 else 0)
    # xmm3 = 2147483647 if xmm3 else 0
    # xmm7 = 2147483647 if xmm7 else 0
    # print(bin(xmm3))
    # print(bin(xmm7))
    xmm4 -= xmm2  # halfnorm - (..8f)  = 1 or 0
    xmm2 = xmm7
    xmm0 = xmm4
    xmm1 = xmm4
    xmm0 *= np.float32(1.570313)
    xmm4 *= np.float32(7.54979e-08)
    xmm1 *= np.float32(0.0004837513)
    xmm6 -= xmm0  # halfnorm -xmm0
    xmm6 -= xmm1  # halfnorm -= xmm1
    xmm1 = np.float32(-0.0)  # copy -0.0 to xmm1
    xmm0 = xmm1
    xmm5 = xmm1
    xmm5 = xmm5 if xmm3 else 0.0
    xmm0 = xmm0 if xmm7 else 0.0
    # xmm5 = i_as_f(f_as_i(xmm5) & xmm3)
    # xmm0 = i_as_f(f_as_i(xmm0) & xmm7)
    xmm3 = np.float32(-0.000195153)  # copy to xmm3
    xmm8 = i_as_f(f_as_i(xmm8) & f_as_i(xmm1))
    xmm1 = xmm7
    xmm6 = i_as_f(f_as_i(xmm6) ^ f_as_i(xmm5))
    xmm6 -= xmm4
    xmm4 = np.float32(2.44332e-005)  # copy from ptr
    xmm6 = i_as_f(f_as_i(xmm6) ^ f_as_i(xmm0))
    xmm0 = xmm6
    xmm0 *= xmm6
    xmm4 *= xmm0
    xmm3 *= xmm0
    xmm4 += np.float32(-0.001388732)
    xmm3 += np.float32(0.008332161)
    xmm4 *= xmm0
    xmm3 *= xmm0
    xmm4 += np.float32(0.04166665)
    xmm3 += np.float32(-0.1666666)
    xmm4 *= xmm0
    xmm4 -= np.float32(0.5)
    xmm4 *= xmm0
    xmm0 *= xmm6
    xmm4 += np.float32(1.0)
    xmm3 *= xmm0

    # changed # xmm1 = i_as_f(~f_as_i(xmm1) & f_as_i(xmm4))  # slight change here
    xmm1 = 0.0 if xmm1 else xmm4
    xmm0 = xmm4
    xmm3 += xmm6
    # changed  # i_as_f(f_as_i(xmm0) & f_as_i(xmm7))
    xmm0 = xmm0 if xmm7 else 0.0
    # get new norm again
    # xmm2 = i_as_f(~f_as_i(xmm2) & f_as_i(xmm3))
    xmm2 = 0.0 if xmm2 else xmm3
    # changed  #  i_as_f(f_as_i(xmm3) & f_as_i(xmm7))
    xmm3 = xmm3 if xmm7 else 0.0
    # get 1.0 float again
    xmm1 = i_as_f(f_as_i(xmm1) | f_as_i(xmm3))
    xmm0 = i_as_f(f_as_i(xmm0) | f_as_i(xmm2))
    xmm1 = i_as_f(f_as_i(xmm1) ^ f_as_i(xmm5))  # xmm1[0] is q
    xmm0 = i_as_f(f_as_i(xmm0) ^ f_as_i(xmm8))  # xmm0 is scale_fac
    return xmm1, xmm0


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

    def show_keys(self, keys, bone_names, bone_name):
        try:
            import matplotlib.pyplot as plt
        except:
            logging.warning("No matplotlib, can't show keys")
            return
        if bone_name in bone_names:
            bone_i = bone_names.index(bone_name)
            plt.plot(keys[:, bone_i, 0], label='X')
            plt.plot(keys[:, bone_i, 1], label='Y')
            plt.plot(keys[:, bone_i, 2], label='Z')
            if len(keys[0, 0]) > 3:
                dt = "Rot"
                plt.plot(keys[:, bone_i, 3], label='Q')
            else:
                dt = "Loc"
            # mark every 32 frame
            plt.vlines(range(0, len(keys[:, bone_i, 0]), 32), -1, 1, colors=(0, 0, 0, 0.2), linestyles='--', label='',)
            title_str = f"{dt} Keys for {bone_name} [{bone_i}]"
            logging.info(f"Showing {title_str}")
            plt.title(title_str)
            plt.legend()
            plt.show()

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

    def show_floats(self, mani_info, name_filter=""):
        try:
            import matplotlib.pyplot as plt
        except:
            logging.warning("No matplotlib, can't show keys")
            return
        logging.info(f"Showing floats")
        k = mani_info.keys
        for f_i, f_name in sorted(enumerate(k.floats_names), key=lambda t: t[1]):
            if name_filter and name_filter not in f_name:
                continue
            plt.plot(k.floats[:, f_i], label=f_name)
        plt.xlabel('Frame')
        plt.ylabel('Value')
        plt.title(f"Float Keys for {mani_info.name}")
        plt.legend()
        plt.show()

    def decompress(self, mani_info, dump=False):
        if bitarray is None:
            raise ModuleNotFoundError("Install the 'bitarray' module to decompress animations")
        ck = mani_info.keys.compressed
        logging.debug(
            f"Decompressing {mani_info.name} with {len(ck.segments)} segments, {mani_info.frame_count} frames")
        ck.pos_bones = np.empty((mani_info.frame_count, mani_info.pos_bone_count, 3), np.float32)
        ck.ori_bones = np.empty((mani_info.frame_count, mani_info.ori_bone_count, 4), np.float32)
        assert ck.pos_bone_count == mani_info.pos_bone_count
        assert ck.ori_bone_count == mani_info.ori_bone_count
        frame_offset = 0
        for segment_i, mb in enumerate(ck.segments):
            # dump compressed segment data if needed
            if dump:
                with open(os.path.join(self.dir, f"{mani_info.name}_{segment_i}.maniskeys"), "wb") as f:
                    f.write(mb.data)
            f = BinStream(mb.data)
            f2 = BinStream(mb.data)
            segment_frames_count = self.get_segment_frame_count(segment_i, mani_info.frame_count)
            # create views into the complete data for this segment
            segment_pos_bones = ck.pos_bones[frame_offset:frame_offset + segment_frames_count]
            segment_ori_bones = ck.ori_bones[frame_offset:frame_offset + segment_frames_count]
            try:
                # this is a jump to the end of the compressed keys
                wavelet_byte_offset = f.read_uint_reversed(16)
                context = KeysContext(f2, wavelet_byte_offset, segment_frames_count)
                self.read_pos_keys(context, f, segment_i, mani_info, segment_frames_count, segment_pos_bones)
                self.read_ori_keys(context, f, segment_i, mani_info, segment_frames_count, segment_ori_bones)
            except:
                logging.exception(f"Reading Segment[{segment_i}] (frames {frame_offset}-{frame_offset+segment_frames_count}) failed at bit {f.pos}, byte {f.pos / 8}, size {len(mb.data)} bytes")
            frame_offset += segment_frames_count
        loc_min = ck.loc_bounds.mins[ck.loc_bound_indices]
        loc_ext = ck.loc_bounds.scales[ck.loc_bound_indices]
        ck.pos_bones *= loc_ext
        ck.pos_bones += loc_min

    def read_pos_keys(self, context, f, segment_i, mani_info, segment_frames_count, segment_pos_bones):
        identity = np.zeros(3, np.float32)
        scale = self.get_pack_scale(mani_info)
        for pos_index, pos_name in enumerate(mani_info.keys.pos_bones_names):
            frame_map = np.zeros(32, dtype=np.uint32)
            raw_keys_storage = np.zeros((52, 3), dtype=np.uint32)
            # not byte aligned
            # defines basic loc value
            # logging.info(f"pos[{pos_index}] {pos_name} at bit {f.pos}")
            vec = self.read_vec3(f)[:3]
            vec *= scale

            # scale_pack = float(scale)
            # the scale per bone is always norm = 0 in acro_run
            scale_pack = self.get_pack_scale(mani_info)
            # which channels are keyframed
            keys_flag = f.read_uint(3)
            keys_flag = StoreKeys.from_value(keys_flag)
            if keys_flag.x or keys_flag.y or keys_flag.z:
                new_wavelets_offset = context.read_wavelet_table(frame_map, segment_frames_count)
                self.read_rel_keys(f, frame_map, keys_flag, raw_keys_storage, new_wavelets_offset)
                # logging.info(f"key {i} = {rel_key_masked}")
                if segment_frames_count > 1:
                    frame_inc = 0
                    # set base keyframe
                    segment_pos_bones[0, pos_index] = vec
                    # set other keyframes
                    last_key_a = identity.copy()
                    last_key_b = identity.copy()
                    key_picked = vec.copy()
                    for out_frame_i in range(1, segment_frames_count):
                        trg_frame_i = frame_map[frame_inc]
                        rel = raw_keys_storage[out_frame_i]
                        out = rel.astype(np.float32)
                        out[:] = self.make_signed(*rel)
                        last_key_delta = (last_key_b - last_key_a) + last_key_b
                        base_plus_delta = last_key_delta + key_picked
                        # todo do something here for base_key_float
                        base_key_float = base_plus_delta
                        # instead of scale_pack, this scale is hard-coded to the corresponding float of 1 / 16383
                        final = base_key_float + out * 6.103888e-05
                        if out_frame_i == trg_frame_i:
                            frame_inc += 1
                            # a key is stored for this frame
                            key_picked = final
                            last_key_a = last_key_b.copy()
                            # this scale uses the calculated scale
                            last_key_b = last_key_delta.copy() + out * scale_pack
                        else:
                            # hold key from previous frame
                            # print(pos_index, segment_i* 32 + out_frame_i)
                            key_picked = final
                            last_key_a = identity.copy()
                            last_key_b = identity.copy()
                            # update scale_pack here, todo check if / what norm is used
                            # apparently also norm = 0 in acro_run, but too many to properly verify that for sucessive bones
                            scale_pack = self.get_pack_scale(mani_info)
                            final = segment_pos_bones[out_frame_i-1, pos_index]
                        segment_pos_bones[out_frame_i, pos_index] = final
                # print(segment_pos_bones[:, pos_index])
            else:
                # set all keyframes
                segment_pos_bones[:, pos_index] = vec
        logging.debug(f"Segment[{segment_i}] loc finished at bit {f.pos}, byte {f.pos / 8}")

    def printm(self, v):
        """print in order of memory register"""
        print(list(reversed(v)))

    def read_ori_keys(self, context, f, segment_i, mani_info, segment_frames_count, segment_ori_bones):
        q_scale = 2 * math.pi  # 6.283185
        epsilon = 1.1920929E-7
        zeros = np.zeros(4, dtype=np.float32)
        identity = zeros.copy()
        identity[3] = 1.0
        scale = self.get_pack_scale(mani_info)
        for ori_index, ori_name in enumerate(mani_info.keys.ori_bones_names):
            # logging.info(context)
            frame_map = np.zeros(32, dtype=np.uint32)
            raw_keys_storage = np.zeros((52, 3), dtype=np.uint32)
            # defines basic rot values
            # logging.info(f"ori[{ori_index}] {ori_name} at bit {f.pos}")
            vec = self.read_vec3(f)
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
                # [0.0, -0.6679229, -0.6209728, -0.11621484]
                # dbg: 0 -0.667924 -0.620973 -0.116215
                quat[3] = q
                # if 0 == ori_index:
                #     self.printm(quat)
                #     # [-0.39340287, -0.6679229, -0.6209728, -0.11621484]
                #     # dbg -0.393401 -0.667924 -0.620973 -0.116215
                # logging.info(f"normed {quat}, scale_fac {scale_fac}, q {q}")
                # print(scale_fac, quat)

            # which channels are keyframed
            keys_flag = f.read_uint(3)
            keys_flag = StoreKeys.from_value(keys_flag)
            if keys_flag.x or keys_flag.y or keys_flag.z:
                new_wavelets_offset = context.read_wavelet_table(frame_map, segment_frames_count)
                self.read_rel_keys(f, frame_map, keys_flag, raw_keys_storage, new_wavelets_offset)
                # logging.info(f"key {i} = {rel_key_masked}")
                if segment_frames_count > 1:
                    frame_inc = 0
                    out = np.zeros(4, float)
                    # print(raw_keys_storage)
                    # set base keyframe
                    # logging.info(f"BASE 0: {quat}, {ori_index}")
                    segment_ori_bones[0, ori_index] = quat
                    last_key_a = zeros.copy()
                    # sign flipping happens here
                    quat_pos = quat * -1 if quat[3] < 0 else quat
                    # set other keyframes
                    for out_frame_i in range(1, segment_frames_count):
                        trg_frame_i = frame_map[frame_inc]
                        if trg_frame_i == out_frame_i:
                            frame_inc += 1
                        # DRINK: base_scaled[0] = key_norm_scaled[0]; (move it from xmm10 to xmm3)
                        # 0.393401 0.667924 0.620973 0.116215  (pos quat)
                        # 0.393628 0.667881 0.620829 0.11646 (previous scaled_inter_vec)
                        # 0.39386 0.667572 0.621088 0.116068 (previous scaled_inter_vec)

                        # self.printm(quat_pos)

                        # RUN: base_scaled[0] = key_norm_scaled[0]; (move it from xmm10 to xmm3)
                        # 0.368874 0.768374 0.519172 0.063197
                        # 0.348637 0.760985 0.538746 0.0954309
                        # 0.330992 0.761229 0.534554 0.15883
                        # 0.343155 0.744444 0.526109 0.226402
                        # 0.376467 0.7073 0.526328 0.284567

                        # [0.36887202, 0.7683748, 0.5191722, 0.06319708]
                        # [0.34863484, 0.76098573, 0.5387461, 0.09543093]
                        # [0.3297259, 0.7576619, 0.5439767, 0.14600949]
                        # [0.32211912, 0.7470182, 0.5468263, 0.19794987]
                        # [0.32207847, 0.72864324, 0.55206347, 0.24611075]
                        # [0.31753445, 0.7085945, 0.559884, 0.28912923]
                        # [0.3078687, 0.68939877, 0.5703008, 0.32357895]
                        # [0.3064593, 0.6663042, 0.58162576, 0.35189915]
                        # [0.32131952, 0.6364012, 0.5850807, 0.3865592]
                        # [0.33619794, 0.6088001, 0.5804841, 0.42352292]
                        # [0.34041068, 0.5904749, 0.5728643, 0.45528728]
                        # [0.341018, 0.5756119, 0.55952185, 0.4891963]
                        # [0.324568, 0.57169163, 0.5480837, 0.51713496]
                        # [0.30257863, 0.56873596, 0.5297939, 0.5516376]
                        # [0.26828268, 0.56750315, 0.52094275, 0.5784317]
                        # [0.22642443, 0.56892043, 0.53473836, 0.5823371]
                        # [0.19152102, 0.57362515, 0.5532106, 0.5729153]
                        # [0.16012295, 0.58576816, 0.5610837, 0.56251353]
                        # [0.11858487, 0.6153204, 0.5591543, 0.5428305]
                        # [0.06978842, 0.6530194, 0.55449384, 0.51110846]
                        # [0.021528289, 0.68566346, 0.54832333, 0.4782716]
                        # [-0.02058941, 0.7089914, 0.54174984, 0.45101488]
                        # [-0.05250007, 0.7226237, 0.53575253, 0.43362197]
                        # [-0.0803341, 0.72050357, 0.5405549, 0.42687413]
                        # [-0.110151604, 0.6983943, 0.56522596, 0.42500785]
                        # [-0.13447537, 0.6683695, 0.5936446, 0.4275333]
                        # [-0.14934096, 0.63544095, 0.62107927, 0.43378872]
                        # [-0.16694918, 0.60123855, 0.6516094, 0.43132976]

                        rel = raw_keys_storage[out_frame_i]
                        out[:3] = self.make_signed(*rel)
                        out[3] = 0.0
                        # self.printm(out)
                        # int key (good)
                        # 0 464 -123 525
                        # 0 191 -316 -112
                        # 0 -162 -148 16
                        # 0 -175 -34 54
                        # 0 -12 109 37

                        # todo figure out logic for scale
                        # scale fac (actually dynamic)
                        # 6.10389e-005 6.10389e-005 6.10389e-005 6.10389e-005
                        # 0.000103384 0.000103384 0.000103384 0.000103384
                        # 0.00015692 0.00015692 0.00015692 0.00015692
                        # 0.000169376 0.000169376 0.000169376 0.000169376
                        # 0.000182325 0.000182325 0.000182325 0.000182325

                        # [0.0, 464.0, -123.0, 525.0]
                        # [0.0, 191.0, -316.0, -112.0]
                        # [0.0, -162.0, -148.0, 16.0]
                        # [0.0, -175.0, -34.0, 54.0]
                        # [0.0, -12.0, 109.0, 37.0]
                        # [0.0, -27.0, 164.0, 2.0]
                        # [0.0, -175.0, -24.0, -28.0]
                        # [0.0, -106.0, -303.0, -83.0]
                        # [0.0, 85.0, -52.0, -94.0]
                        # [0.0, 129.0, 201.0, -73.0]
                        # [0.0, 117.0, 7.0, -49.0]
                        # [0.0, 152.0, 311.0, 21.0]
                        # [0.0, 174.0, -40.0, 9.0]
                        # [0.0, -29.0, 241.0, 146.0]
                        # [0.0, -328.0, 402.0, 159.0]
                        # [0.0, -214.0, 112.0, -101.0]
                        # [0.0, 81.0, 14.0, -203.0]
                        # [0.0, 148.0, 317.0, -185.0]
                        # [0.0, 3.0, 255.0, -61.0]
                        # [0.0, -9.0, -37.0, 24.0]
                        # [0.0, -19.0, -191.0, 33.0]
                        # [0.0, -32.0, -277.0, 14.0]
                        # [0.0, -18.0, -283.0, 228.0]
                        # [0.0, -46.0, -206.0, 419.0]
                        # [0.0, -34.0, -163.0, 70.0]
                        # [0.0, -54.0, -151.0, -57.0]
                        # [0.0, -79.0, 102.0, 86.0]
                        # [0.0, 95.0, 157.0, -19.0]


                        # RUN: scaled rel key (xmm12)
                        # 0 0.028322 -0.00750778 0.0320454
                        # 0 0.0197464 -0.0326694 -0.011579
                        # 0 -0.025421 -0.0232242 0.00251072
                        # 0 -0.0296407 -0.00575877 0.00914628
                        # 0 -0.0021879 0.0198734 0.00674601
                        # [0.0, 0.028322041, -0.0075077824, 0.032045413]
                        # [0.0, 0.011658426, -0.019288287, -0.0068363547]
                        # [0.0, -0.009888299, -0.0090337545, 0.0009766221]
                        # [0.0, -0.010681804, -0.002075322, 0.0032960996]
                        # [0.0, -0.0007324666, 0.006653238, 0.0022584386]
                        # [0.0, -0.0016480498, 0.010010377, 0.00012207776]
                        # [0.0, -0.010681804, -0.0014649332, -0.0017090887]
                        # [0.0, -0.0064701214, -0.018494781, -0.005066227]
                        # [0.0, 0.005188305, -0.0031740218, -0.005737655]
                        # [0.0, 0.007874016, 0.012268815, -0.0044558384]
                        # [0.0, 0.007141549, 0.00042727217, -0.0029909052]
                        # [0.0, 0.00927791, 0.018983092, 0.0012818165]
                        # [0.0, 0.010620765, -0.0024415553, 0.00054934993]
                        # [0.0, -0.0017701276, 0.01471037, 0.008911677]
                        # [0.0, -0.020020753, 0.02453763, 0.009705182]
                        # [0.0, -0.013062321, 0.0068363547, -0.006164927]
                        # [0.0, 0.0049441494, 0.00085454434, -0.012390893]
                        # [0.0, 0.0090337545, 0.019349325, -0.011292193]
                        # [0.0, 0.00018311664, 0.015564915, -0.0037233718]
                        # [0.0, -0.00054934993, -0.0022584386, 0.0014649332]
                        # [0.0, -0.0011597387, -0.011658426, 0.002014283]
                        # [0.0, -0.0019532442, -0.01690777, 0.00085454434]
                        # [0.0, -0.0010986999, -0.017274003, 0.013916865]
                        # [0.0, -0.0028077886, -0.01257401, 0.025575291]
                        # [0.0, -0.002075322, -0.009949338, 0.0042727217]
                        # [0.0, -0.0032960996, -0.009216871, -0.0034792162]
                        # [0.0, -0.0048220716, 0.006225966, 0.005249344]
                        # [0.0, 0.0057986937, 0.009583104, -0.0011597387]
                        # RUN: adder (xmm9)
                        # 0 0 0 0
                        # 0 0.028322 -0.00750778 0.0320454
                        # 0 0.0480684 -0.0401772 0.0204664
                        # 0 0.0226474 -0.0634013 0.0229771
                        # 0 -0.00699335 -0.0691601 0.0321234

                        # DRINK: scaled rel key (xmm12)
                        # 0 0 -0.000366233 0
                        # 0 -0.00054935 0.00054935 0.000183117
                        # 0 0 0.000305194 -0.000183117
                        # DRINK: adder (xmm9)
                        # 0 0 0 0
                        # 0 0 -0.000366233 0 (last_key_a)
                        # 0 -0.00054935 0.000183117 0.000183117

                        scaled_rel_key = out * scale_pack
                        # self.printm(scaled_rel_key)
                        # self.printm(last_key_a)
                        # these are ok
                        out = scaled_rel_key + last_key_a
                        q = math.sqrt(max(0.0, 1.0 - np.sum(np.square(out))))
                        # q stays 0.0
                        rel_scaled = out.copy()
                        rel_scaled_q = out.copy()
                        rel_scaled_q[3] = q

                        # RUN: rel_scaled assignment of Q done
                        # 0.999057 0.028322 -0.00750778 0.0320454
                        # 0.997826 0.0480684 -0.0401772 0.0204664
                        # 0.997467 0.0226474 -0.0634013 0.0229771
                        # 0.997064 -0.00699335 -0.0691601 0.0321234
                        # 0.997986 -0.00918124 -0.0492867 0.0388694

                        # [0.9990569, 0.028322041, -0.0075077824, 0.032045413]
                        # [0.99852294, 0.039980467, -0.026796069, 0.025209058]
                        # [0.99856144, 0.030092169, -0.035829823, 0.02618568]
                        # [0.9986577, 0.019410364, -0.037905145, 0.02948178]
                        # [0.9988328, 0.018677898, -0.031251907, 0.03174022]
                        # [0.9991214, 0.017029848, -0.02124153, 0.031862296]
                        # [0.99926716, 0.0063480437, -0.022706464, 0.030153207]
                        # [0.99883586, -0.00012207776, -0.041201245, 0.02508698]
                        # [0.9988147, 0.005066227, -0.044375267, 0.019349325]
                        # [0.9992897, 0.012940243, -0.03210645, 0.014893487]
                        # [0.99922544, 0.020081792, -0.03167918, 0.011902582]
                        # [0.99940133, 0.029359702, -0.012696087, 0.013184398]
                        # [0.9989914, 0.039980467, -0.015137643, 0.013733748]
                        # [0.999013, 0.03821034, -0.00042727217, 0.022645425]
                        # [0.99902016, 0.018189587, 0.024110358, 0.032350607]
                        # [0.9991648, 0.005127266, 0.030946713, 0.02618568]
                        # [0.9993483, 0.010071415, 0.031801257, 0.013794787]
                        # [0.99850506, 0.01910517, 0.051150583, 0.0025025941]
                        # [0.9975848, 0.019288287, 0.066715494, -0.0012207776]
                        # [0.9977445, 0.018738937, 0.06445706, 0.00024415553]
                        # [0.9984479, 0.017579198, 0.052798633, 0.0022584386]
                        # [0.9992287, 0.015625954, 0.035890862, 0.003112983]
                        # [0.9995761, 0.014527254, 0.018616859, 0.017029848]
                        # [0.99900496, 0.011719465, 0.0060428493, 0.04260514]
                        # [0.9988464, 0.009644143, -0.0039064884, 0.04687786]
                        # [0.9989515, 0.0063480437, -0.0131233595, 0.043398645]
                        # [0.998791, 0.001525972, -0.0068973936, 0.04864799]
                        # [0.99884135, 0.007324666, 0.0026857108, 0.04748825]

                        # rel_scaled_q differs from scaled_rel_key
                        # DRINK: rel_scaled assignment of Q done
                        # 1 0 -0.000366233 0
                        # 1 -0.00054935 0.000183117 0.000183117
                        # 1 -0.00054935 0.000488311 0
                        # good
                        # [0.99999994, 0.0, -0.0003662333, 0.0]
                        # [0.9999998, -0.00054934993, 0.00018311664, 0.00018311664]
                        # [0.9999997, -0.00054934993, 0.00048831105, 0.0]

                        # self.printm(rel_scaled_q)
                        # if out_frame_i == 3:
                        #     return
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
                        # until here, scaled_inter should be fine as the first frame is good
                        # for those observed: norm = 1, 1, 1, 1
                        # norm * rel_inter 1: 0.393628 0.667881 0.620829 0.11646
                        # norm * rel_inter 2: 0.39386 0.667572 0.621088 0.116068
                        # norm * rel_inter 3: 0.393923 0.667412 0.621344 0.115401
                        # norm * rel_inter 4: 0.393962 0.667174 0.621778 0.1143
                        # norm * rel_inter 5: 0.393895 0.666904 0.622377 0.11284

                        # current state, 1 is fine for root joint
                        # [0.3936303, 0.66788036, 0.62082875, 0.11645946]
                        # [0.39340726, 0.6676567, 0.6213749, 0.115578786]
                        # [0.39159092, 0.6687292, 0.6216812, 0.11388766]
                        # [0.38193962, 0.66985697, 0.62824786, 0.10352965]
                        # [0.3212125, 0.67668223, 0.6612884, 0.040267248]

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
                        # last_key_a is
                        # 0 0 -0.000366233 0
                        # 0 -0.00054935 0.000183117 0.000183117
                        # 0 -0.00054935 0.000488311 0
                        # 0 -0.000854544 0.000854544 0
                        # 0 -0.00103766 0.00122078 0
                        # 0 -0.00103766 0.00146493 0.000122078
                        # 0 -0.00134286 0.00146493 0.000122078
                        # 0 -0.00134286 0.00183117 0.000122078

                        # store scaled_inter_vec from xmm9 on ptr
                        # round 1
                        # xmm9 0.393628 0.667881 0.620829 0.11646 (scaled_inter_vec)
                        # xmm13 -0.393401 -0.667924 -0.620973 -0.116215 (quat)
                        # round 2
                        # xmm9 0.39386 0.667572 0.621088 0.116068 (scaled_inter_vec)
                        # xmm13 0.393628 0.667881 0.620829 0.11646 (NOT quat but previous scaled_inter_vec)
                        # round 3
                        # xmm9 0.393923 0.667412 0.621344 0.115401 (scaled_inter_vec)
                        # xmm13 0.39386 0.667572 0.621088 0.116068 (NOT quat but previous scaled_inter_vec)
                        # round 4
                        # xmm9 0.393962 0.667174 0.621778 0.1143 (scaled_inter_vec)
                        # xmm13 0.393923 0.667412 0.621344 0.115401 (NOT quat but previous scaled_inter_vec)

                        last_key_a = zeros.copy() if which_key_flag else rel_scaled_clamped_copy.copy()
                        # last_key_a = identity.copy() if not which_key_flag else rel_scaled_clamped_copy.copy()

                        # store last_key_a on ptr
                        # 0 0 -0.000366233 0
                        # 0 -0.00054935 0.000183117 0.000183117
                        # 0 -0.00054935 0.000488311 0
                        # 0 -0.000854544 0.000854544 0


                        # if 0 == ori_index:
                        # [0.0, 0.0, -0.0003662333, 0.0]
                        # [0.0, -0.00054934993, -0.0027467497, 0.00018311664]
                        # [0.0, -0.0, -0.013428554, -0.0007324666]
                        #     # [0.0, 0.0, -0.0003662333, 0.0]
                        #     # [0.0, -0.00054934993, -0.0027467497, 0.00018311664]
                        #     # [0.0, -0.0, -0.013428554, -0.0007324666]
                        #     # [0.0, -0.0003051944, -0.08020509, -0.0]
                        #     # [0.0, 0.0007324666, -0.4808643, 0.0]
                        # self.printm(last_key_a)
                        if do_increment:
                            final_inter = scaled_inter
                            # use scaled_inter_vec_copy
                        else:
                            # todo another round of clamping
                            # transfer signs from sign_source, store on ptr_to_final?
                            # use recon quat instead
                            final_inter = quat_pos

                        # store final xmm13 on ptr (equivalent to scaled_inter_vec from above)
                        # 0.393628 0.667881 0.620829 0.11646
                        # 0.39386 0.667572 0.621088 0.116068
                        # 0.393923 0.667412 0.621344 0.115401
                        # 0.393962 0.667174 0.621778 0.1143

                        # self.printm(final_inter)
                        # quat aka recon_quat is set to last key of curve for the next loop, todo verify
                        quat_pos = final_inter
                        # logging.info(f"INTER {out_frame_i}: {final_inter}, {ori_index}")
                        segment_ori_bones[out_frame_i, ori_index, ] = final_inter
                    # break
            else:
                # set all keyframes
                segment_ori_bones[:, ori_index] = quat
        logging.debug(f"Segment[{segment_i}] rot finished at bit {f.pos}, byte {f.pos / 8}")

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

    def read_rel_keys(self, f, frame_map, keys_flag, raw_keys_storage, new_wavelets_offset):
        for channel_i, is_active in enumerate((keys_flag.x, keys_flag.y, keys_flag.z)):
            if is_active:
                # logging.info(f"rel_keys[{channel_i}] at bit {f.pos}")
                # define the minimal key size for this channel
                ch_key_size = f.read_uint_reversed(4)
                ch_key_size_masked = ch_key_size & 31
                assert ch_key_size <= 32
                # logging.info(f"channel[{channel_i}] base_size {ch_key_size} at bit {f.pos}")
                for trg_frame_i in frame_map[:new_wavelets_offset]:
                    rel_key_flag = 1 << ch_key_size_masked | 1 >> (32 - ch_key_size_masked)
                    # rel_key_size = f.read_bit_size_flag(15 - ch_key_size_masked)
                    rel_key_size = f.read_bit_size_flag(32)
                    # todo this may have to be shifted only with the corresponding clamp applied
                    rel_key_base = f.interpret_as_shift(rel_key_size, rel_key_flag)
                    ch_rel_key_size = ch_key_size + rel_key_size
                    # clamp key size to 0-15 bits
                    ch_rel_key_size = min(ch_rel_key_size, 15)
                    # ensure the final key size is valid
                    assert ch_rel_key_size <= 32
                    # logging.info(f"ch_rel_key_size {ch_rel_key_size}")
                    # read the key, if it has a size
                    if ch_rel_key_size:
                        ch_rel_key = f.read_uint_reversed(ch_rel_key_size)
                    else:
                        ch_rel_key = 0
                    # logging.info(f"key = {ch_rel_key}")
                    rel_key_masked = (rel_key_base + ch_rel_key) & 0xffff
                    raw_keys_storage[trg_frame_i, channel_i] = rel_key_masked

    def read_vec3(self, f):
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
        vec[:] = self.make_signed(x, y, z, 0)
        return vec

    def make_signed(self, *args):
        return [-(x + 1 >> 1) if x & 1 else x >> 1 for x in args]


def get_quat_scale_fac2(norm_half_abs):
    flip_scale = norm_half_abs < 0.0  # input is generally positive as it comes from a norm
    clamped = np.abs(np.float32(norm_half_abs))
    clamped = clamped % (2*np.pi)  # wrap to 2pi range
    quadrant = round(clamped * 0.6366197)  # 0.6366197 ~ 2 / pi
    flip_q = quadrant in (2.0, 3.0)
    wrap_phase = quadrant in (1.0, 3.0)
    x = clamped - quadrant * np.float32(1.570313)  # very close to pi/2
    x -= quadrant * np.float32(0.0004837513)
    x = -x if wrap_phase else x
    x -= quadrant * np.float32(7.54979e-08)
    x = -x if flip_q else x
    scale = x * x
    a = (np.float32(2.44332e-005) * scale + np.float32(-0.001388732)) * scale + np.float32(0.04166665)
    b = (np.float32(-0.000195153) * scale + np.float32(0.008332161)) * scale + np.float32(-0.1666666)
    a *= scale
    a -= np.float32(0.5)
    a *= scale
    scale *= x
    a += np.float32(1.0)
    b *= scale
    b += x
    q = b if wrap_phase else a
    scale = a if wrap_phase else b
    q = -q if flip_q else q
    scale = -scale if flip_scale else scale
    return q, scale


def test_get_scale_fac():
    # inp = np.arange(0, 4 * math.pi, math.pi*0.1)
    # inp = np.arange(0, 2 * math.pi, math.pi*0.1)
    inp = np.arange(0, 4 * math.pi, math.pi*0.01)
    q_data = np.zeros(len(inp))
    s_data = np.zeros(len(inp))
    q2_data = np.zeros(len(inp))
    s2_data = np.zeros(len(inp))
    for i, x in enumerate(inp):
        q_data[i], s_data[i] = get_quat_scale_fac(x)
        q2_data[i], s2_data[i] = get_quat_scale_fac2(x)
    assert np.allclose(q_data, q2_data, rtol=1e-03, atol=1e-05, equal_nan=False)
    assert np.allclose(s_data, s2_data, rtol=1e-03, atol=1e-05, equal_nan=False)
    import matplotlib.pyplot as plt
    plt.plot(inp, q_data, label="Q")
    plt.plot(inp, s_data, label="S")
    plt.plot(inp, q2_data, label="Q2", linestyle='-.')
    plt.plot(inp, s2_data, label="S2", linestyle='-.')
    plt.xlabel('Input')
    plt.ylabel('Value')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    logging_setup("mani")
    for k in (0, 1, 4, 5, 6, 8, 9, 14, 32, 34, 36, 37, 38, 64, 66, 68, 69, 70, 82, 48, 112, 113, 114):
        print(ManisDtype.from_value(k))
    mani = ManisFile()
    # mani.load("C:/Users/arnfi/Desktop/motionextracted.maniset48183260.manis")
    # mani.parse_keys("giganotosaurusjw@walk", dump=True)
    # mani.load("C:/Users/arnfi/Desktop/indominus/motionextracted.maniset39f6a438.manis")
    # WH
    # mani.load("C:/Users/arnfi/Desktop/animation.manisetb22bfc73.manis")  # first is uncompressed
    # mani.load("C:/Users/arnfi/Desktop/animation.maniset273472b1.manis")
    # print(mani)
    # ZTUAC
    # mani.load("C:/Users/arnfi/Desktop/locomotion.maniset4838180b.manis")
    # print(mani)
    # mani.load("C:/Users/arnfi/Desktop/pyro/motionextracted.maniset846adda6.manis")
    # mani.load("C:/Users/arnfi/Desktop/anky_JWE1/fighting.maniset5969e5be.manis")
    # mani.load("C:/Users/arnfi/Desktop/acro/motionextracted.maniset935739f8.manis")
    # mani.load("C:/Users/arnfi/Desktop/Coding/Frontier/Warhammer/Annihilator/animation.maniset52a766ac.manis")
    # mani.load("C:/Users/arnfi/Desktop/enrichment.maniset8a375fce.manis")
    # mani.load("C:/Users/arnfi/Desktop/camerabone.maniset67b9ba24.manis")
    # print(mani)
    # mani.load("C:/Users/arnfi/Desktop/motionextracted.maniset1d7ef17e.manis")
    # mani.load("C:/Users/arnfi/Desktop/locomotion.manisetdd6f52f3.manis")
    # mani.load("C:/Users/arnfi/Desktop/test.manis")
    # print(mani)

    # mani.load("C:/Users/arnfi/Desktop/animationmotionextractedlocomotion.maniset648a1a01.manis")
    # mani.load("C:/Users/arnfi/Desktop/crane/animationnotmotionextractedfighting.maniset3d816f2c.manis")
    # mani.load("C:/Users/arnfi/Desktop/swan/animationmotionextractedbehaviour.maniset86a13695.manis")
    # mani.load("C:/Users/arnfi/Desktop/animation.maniset293c241f.manis")
    # print(mani)
    # mani.load("C:/Users/arnfi/Desktop/Wheel/animation.maniset9637aeb4.manis")
    # mani.load("C:/Users/arnfi/Desktop/DLA scale anim.manis")
    # mani.load("C:/Users/arnfi/Desktop/dinomascot/animation.maniset293c241f.manis")
    # mani.dump_keys()

    # mani.load("C:/Users/arnfi/Desktop/acro/notmotionextracted.maniset53978456.manis")  # stationary anims
    # # mani.parse_keys("acrocanthosaurus@standidle01")
    # mani.parse_keys("acrocanthosaurus@drinksocialinteractiona")

    # mani.load("C:/Users/arnfi/Desktop/motionextracted.maniset85c65403.manis")  # locomotion
    # # todo debug acrocanthosaurus@walk - def_horselink_joint_IKBlend.L segment[0] loc, segment[1] is fine
    # maybe create a dedicated copy of walk that includes just that bone?
    # mani.parse_keys("acrocanthosaurus@walk")

    # # JWE1
    # mani.load("C:/Users/arnfi/Desktop/anky_JWE1/fighting.maniset2b08396d.manis")  # fighting
    # print(mani)
    # mani.parse_keys("ankylosaurus@standidle01")
    # mani.load("C:/Users/arnfi/Desktop/notmotionextracted.manisetb28920cd.manis")  # stationary
    # mani.parse_keys("ankylosaurus@standidle01")
    # mani.load("C:/Users/arnfi/Desktop/locomotion.manisetdd6f52f3.manis")  # locomotion
    # mani.parse_keys("ankylosaurus@walkbase")

    # # JWE2
    # # mani.load("C:/Users/arnfi/Desktop/notmotionextracted.maniset81182102.manis")
    # # mani.parse_keys("ankylosaurus@standidlexx")
    # mani.load("C:/Users/arnfi/Desktop/motionextracted.maniset6dfd5af.manis")  # locomotion
    # mani.parse_keys("ankylosaurus@walk")

    # # PZ old
    # mani.load("C:/Users/arnfi/Desktop/animationmotionextractedlocomotion.manisete954492e_old.manis")  # locomotion
    # mani.parse_keys("bengal_tiger_male@walkbase")
    #
    # # PZ new
    # mani.load("C:/Users/arnfi/Desktop/animationmotionextractedlocomotion.manisete954492e_new.manis")  # locomotion
    # mani.parse_keys("bengal_tiger_male@walkbase")

    # mani.load("C:/Users/arnfi/Desktop/acro/motionextracted.maniset935739f8.manis")  # hatchery anims
    # mani.parse_keys("acrocanthosaurus@hatcheryexit_01")
    # mani.log_rot_keys()
    # mani.log_loc_keys()
    # test_get_scale_fac()
# mani.load("C:/Users/arnfi/Desktop/donationbox/animation.maniseteaf333c5.manis")
# mani.dump_keys()
# mani.parse_keys()
# # mani.load("C:/Users/arnfi/Desktop/gate/animation.manisetd2b36ae0.manis")
# print(mani)
# # mani.load("C:/Users/arnfi/Desktop/JWE2/pyro/hatcheryexitcamera.maniset8c6441b9.manis")
# mani.parse_keys()
# mani.load("C:/Users/arnfi/Desktop/dilo/locomotion.maniset1c05e0f4.manis")
# mani.load("C:/Users/arnfi/Desktop/ostrich/ugcres.maniset8982114c.manis")
# mani.load("C:/Users/arnfi/Desktop/Coding/ovl/OVLs/anim test/rot_x_0_22_42.manis")
# mani.load("C:/Users/arnfi/Desktop/Coding/ovl/OVLs/anim test/ugcres.maniset8982114c0.manis")
# mani.load("C:/Users/arnfi/Desktop/Coding/ovl/OVLs/anim test/ugcres.maniset8982114c1.manis")
# mani.load("C:/Users/arnfi/Desktop/Coding/ovl/OVLs/anim test/ugcres.maniset8982114c2.manis")
# mani.load("C:/Users/arnfi/Desktop/Coding/ovl/PZ 1.6/anim/animation.maniset9637aeb4.manis")
# mani.load("C:/Users/arnfi/Desktop/Coding/ovl/PZ 1.6/anim/animationmotionextractedbehaviour.maniset5f721adf.manis")
# mani.load("C:/Users/arnfi/Desktop/Coding/ovl/PZ 1.6/anim/animationmotionextractedlocomotion.maniset58076276.manis")
# mani.load("C:/Users/arnfi/Desktop/lemur/animationnotmotionextractedpartials.maniset919dac12.manis")
# mani.load("C:/Users/arnfi/Desktop/lemur/animationmotionextractedfighting.maniset9c749130.manis")
# mani.load("C:/Users/arnfi/Desktop/lemur/animationnotmotionextractedlocomotion.maniset87d072d8.manis")

# mani.load("C:/Users/arnfi/Desktop/Coding/Frontier/anim/wheel/animation.maniset9637aeb4.manis")

# mani.load("C:/Users/arnfi/Desktop/Coding/Frontier/anim/Iron_piston/ugcres.maniset8982114c.manis")
# mani.load("C:/Users/arnfi/Desktop/Coding/Frontier/anim/pc dino/animation.maniset293c241f.manis")

# mani.load("C:/Users/arnfi/Desktop/Coding/Frontier/anim/dilo/notmotionextracted.manisetf2b1fd43.manis")  # ok 0000 24 bytes f
# mani.load("C:/Users/arnfi/Desktop/Coding/Frontier/anim/dilo/motionextracted.maniset1823adb0.manis")  # 0111 48 bytes f
# mani.load("C:/Users/arnfi/Desktop/Coding/Frontier/anim/dilo/motionextracted.maniset1bfb6052.manis")  # 0, 2, 3, 1

# mani.load("C:/Users/arnfi/Desktop/Coding/Frontier/anim/ceara/hatcheryexitcamera.maniset9762d823.manis")
# mani.load("C:/Users/arnfi/Desktop/Coding/Frontier/anim/ceara/motionextracted.maniset7e6b0db3.manis") # keys are external
# mani.load("C:/Users/arnfi/Desktop/Coding/Frontier/anim/ceara/motionextracted.manisetf2b6c52d.manis")
# print(mani)

# mani.load("C:/Users/arnfi/Desktop/manis/fee_feeder_ground.maniset2759dfaf.manis")
# mani.load("C:/Users/arnfi/Desktop/manis/motionextracted.maniset167ed454.manis")
