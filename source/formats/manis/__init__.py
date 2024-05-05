import contextlib
import logging
import math
import struct
import os
import numpy as np
np.set_printoptions(precision=4, suppress=True)

import root_path
from generated.formats.manis.bitfields.ManisDtype import ManisDtype
from ovl_util.logs import logging_setup
from generated.formats.manis.bitfields.StoreKeys import StoreKeys
from generated.formats.manis.compounds.InfoHeader import InfoHeader
from generated.io import IoFile

try:
    import bitarray
    import bitarray.util
except:
    bitarray = None
    logging.warning(f"bitarray module is not installed")

# np.set_printoptions(suppress=True, precision=4)


def swap16(i):
    return struct.unpack("<h", struct.pack(">h", i))[0]


def hex_test():
    for i in range(20):
        x = 2 ** i
        print(i, bin(i), x, bin(x))


class BinStream:
    def __init__(self, val):
        self.data = bitarray.bitarray(endian='little')
        self.data.frombytes(val)
        self.pos = 0

    def seek(self, pos):
        self.pos = pos

    def read(self, size):
        d = self.data[self.pos: self.pos + size]
        assert len(d) == size, f"Reached end of chunk reading {size} bits at {self.pos}"
        self.pos += size
        return d

    def read_int(self, size):
        bits = self.read(size)
        return bitarray.util.ba2int(bits, signed=True)

    def read_uint(self, size):
        bits = self.read(size)
        return bitarray.util.ba2int(bits, signed=False)

    # return bitarray.util.int2ba(0x99c51a50c66, length=45, endian="little", signed=False)

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
    def __init__(self, f2, wavelet_byte_offset):
        # logging.info(f"wavelet_byte_offset {wavelet_byte_offset}")
        f2.seek(wavelet_byte_offset * 8)
        self.do_increment = f2.read_uint(1)
        self.runs_remaining = f2.read_uint(16)
        # size = k_channel_bitsize + 1
        # verified
        size = 4
        self.init_k_a = f2.read_uint_reversed(size)
        self.init_k_b = f2.read_uint_reversed(size)
        if not self.do_increment:
            self.init_k_a, self.init_k_b = self.init_k_b, self.init_k_a
        logging.info(self)
        self.do_increment = not self.do_increment
        self.begun = True
        self.i_in_run = 0

    def __repr__(self):
        return f"do_increment {self.do_increment}, runs_remaining {self.runs_remaining}, init_k_a {self.init_k_a}, init_k_b {self.init_k_b}"


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
    xmm4 *= np.float32(0.63662)  # halfnorm
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
    xmm0 *= np.float32(1.57031)
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
    xmm4 += np.float32(-0.00138873)
    xmm3 += np.float32(0.00833216)
    xmm4 *= xmm0
    xmm3 *= xmm0
    xmm4 += np.float32(0.0416666)
    xmm3 += np.float32(-0.166667)
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

    def load(self, filepath):
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

    def get_bitsize(self):
        # for i in reversed(range(31, -1, -1)):
        # 	# print(i, 15 >> i)
        # 	if 15 >> i == 0:
        # 		return i
        # return -1
        new_bit = 0xf  # MOV new_bit,0xf
        # return new_bit.bit_length()  # - 1
        return new_bit.bit_length() - 1

    def segment_frame_count(self, i, frame_count):
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

    def parse_keys(self, target=None):
        for mani_info in self.iter_compressed_manis():
            keys_iter = None
            if target and mani_info.name != target:
                continue
            # acro debug keys
            dump_path = os.path.join(root_path.root_dir, "dumps", f"{mani_info.name}_keys.txt")
            if os.path.isfile(dump_path):
                logging.info(f"Found reference keys for {mani_info.name}")
                keys = [int(line.strip(), 0) for line in open(dump_path, "r")]
                keys_iter = iter(keys)
            # logging.info(mani_info)
            # logging.info(mani_info.keys.compressed)
            try:
                self.decompress(keys_iter, mani_info)
            except:
                logging.exception(f"Decompressing {mani_info.name} failed")

    def show_keys(self, keys, bone_names, bone_name):
        try:
            import matplotlib.pyplot as plt
        except:
            logging.warning("No matplotlib, can't show keys")
            return
        if bone_name in bone_names:
            logging.info(f"Showing keys")
            bone_i = bone_names.index(bone_name)
            # plt.figure(figsize=(5, 2.7), layout='constrained')
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
            plt.xlabel('Frame')
            plt.ylabel('Value')
            plt.title(f"{dt} Keys for {bone_name}")
            plt.legend()
            plt.show()

    def show_floats(self, name_filter=""):
        try:
            import matplotlib.pyplot as plt
        except:
            logging.warning("No matplotlib, can't show keys")
            return
        logging.info(f"Showing floats")
        for mani_info in self.mani_infos:
            k = mani_info.keys
            for f_i, f_name in enumerate(k.floats_names):
                if name_filter and name_filter not in f_name:
                    continue
                plt.plot(k.floats[:, f_i], label=f_name)
            plt.xlabel('Frame')
            plt.ylabel('Value')
            plt.title(f"Float Keys for {mani_info.name}")
            plt.legend()
            plt.show()

    def decompress(self, keys_iter, mani_info):
        if bitarray is None:
            raise ModuleNotFoundError("bitarray module is not installed - cannot decompress keys")
        k_channel_bitsize = self.get_bitsize()
        k = mani_info.keys
        ck = mani_info.keys.compressed
        logging.info(
            f"Anim {mani_info.name} with {len(ck.segments)} segments, {mani_info.frame_count} frames")
        ck.pos_bones = np.empty((mani_info.frame_count, mani_info.pos_bone_count, 3), np.float32)
        ck.ori_bones = np.empty((mani_info.frame_count, mani_info.ori_bone_count, 4), np.float32)
        assert ck.pos_bone_count == mani_info.pos_bone_count
        assert ck.ori_bone_count == mani_info.ori_bone_count
        frame_offset = 0
        for segment_i, mb in enumerate(ck.segments):
            f = BinStream(mb.data)
            f2 = BinStream(mb.data)
            segment_frames_count = self.segment_frame_count(segment_i, mani_info.frame_count)
            # logging.info(f"Segment[{segment_i}] frames {segment_frames_count} Keys Iter {keys_iter}")
            # create views into the complete data for this segment
            segment_pos_bones = ck.pos_bones[frame_offset:frame_offset + segment_frames_count]
            segment_ori_bones = ck.ori_bones[frame_offset:frame_offset + segment_frames_count]
            try:
                # this is a jump to the end of the compressed keys
                wavelet_byte_offset = f.read_uint_reversed(16)
                context = KeysContext(f2, wavelet_byte_offset)
                self.read_vec3_keys(context, f, f2, segment_i, k_channel_bitsize, mani_info,
                                    segment_frames_count, segment_pos_bones, keys_iter=keys_iter)
                self.read_rot_keys(context, f, f2, segment_i, k_channel_bitsize, mani_info, segment_frames_count,
                                   segment_ori_bones, keys_iter=keys_iter)
            except:
                logging.exception(f"Reading Segment[{segment_i}] failed at bit {f.pos}, byte {f.pos / 8}")
                raise
            frame_offset += segment_frames_count
        loc_min = ck.loc_bounds.mins[ck.loc_bound_indices]
        loc_ext = ck.loc_bounds.scales[ck.loc_bound_indices]
        ck.pos_bones *= loc_ext
        ck.pos_bones += loc_min
        # self.show_keys(ck.ori_bones, k.ori_bones_names, "def_l_legUpr_joint")  # first bone in run anim
        # self.show_keys(ck.ori_bones, k.ori_bones_names, "def_c_root_joint")
        # self.show_keys(ck.ori_bones, k.ori_bones_names, "srb")
        # self.show_keys(ck.ori_bones, k.ori_bones_names, "def_c_spine0_joint")
        # self.show_keys(ck.pos_bones, k.pos_bones_names, "def_c_root_joint")
        self.show_keys(ck.pos_bones, k.pos_bones_names, "srb")
        # self.show_keys(ck.pos_bones, k.pos_bones_names, "def_l_horselink_joint_IKBlend")
        # logging.info(ck)
        # for pos_index, pos_name in enumerate(mani_info.keys.pos_bones_names):
        #     logging.info(f"dec {pos_index} {pos_name} {loc[0, pos_index]}")

    def read_vec3_keys(self, context, f, f2, i, k_channel_bitsize, mani_info,
                       segment_frames_count, segment_pos_bones, keys_iter=None):
        identity = np.zeros(3, np.float32)
        scale = self.get_pack_scale(mani_info)
        for pos_index, pos_name in enumerate(mani_info.keys.pos_bones_names):
            frame_map = np.zeros(32, dtype=np.uint32)
            ushort_storage = np.zeros(156, dtype=np.uint32)
            # definitely not byte aligned as the key bytes can not be found in the manis data
            # defines basic loc values and which channels are keyframed
            # logging.info(f"pos[{pos_index}] {pos_name} at bit {f.pos}")
            f_pos = f.pos
            pos_base, vec = self.read_vec3(f)
            vec *= scale

            # scale_pack = float(scale)
            # the scale per bone is always norm = 0 in acro_run
            scale_pack = self.get_pack_scale(mani_info)
            # logging.info(f"{pos_index} {pos_name} {vec}")
            # logging.info(f"{(x, y, z)} {struct.pack('f', x), struct.pack('f', y), struct.pack('f', z)}")
            self.compare_key_with_reference(f, keys_iter, pos_base)
            keys_flag = f.read_uint_reversed(3)
            keys_flag = StoreKeys.from_value(keys_flag)
            # if pos_name == "def_c_root_joint":
            #     logging.info(f"{keys_flag}")
            if keys_flag.x or keys_flag.y or keys_flag.z:
                wavelet_i, frame_map = self.read_wavelet_table(context, f2, frame_map, segment_frames_count)
                self.read_rel_keys(f, frame_map, k_channel_bitsize, keys_flag, ushort_storage, wavelet_i)
                # logging.info(f"key {i} = {rel_key_masked}")
                if segment_frames_count > 1:
                    frame_inc = 0
                    # set base keyframe
                    segment_pos_bones[0, pos_index] = vec[:3]
                    # set other keyframes
                    last_key_a = identity.copy()
                    last_key_b = identity.copy()
                    key_picked = vec[:3].copy()
                    for out_frame_i in range(1, segment_frames_count):
                        trg_frame_i = frame_map[frame_inc]
                        if trg_frame_i == out_frame_i:
                            frame_inc += 1
                        rel = ushort_storage[out_frame_i*3: out_frame_i*3+3]
                        out = rel.astype(np.float32)
                        out[0] = self.make_signed(rel[0])
                        out[1] = self.make_signed(rel[1])
                        out[2] = self.make_signed(rel[2])
                        last_key_delta = (last_key_b - last_key_a) + last_key_b
                        base_plus_delta = last_key_delta + key_picked
                        # todo do something here for base_key_float
                        base_key_float = base_plus_delta
                        # instead of scale_pack, this scale is hard-coded to the corresponding float of 1 / 16383
                        final = base_key_float + out * 6.103888e-05

                        next_key_offset = 0 if out_frame_i == trg_frame_i else 4
                        # assuming that DAT_7ff7077fd480 is just a pointer to 0, FF int used as a masking cond
                        which_key_flag = True if next_key_offset else False
                        key_picked = vec[:3] if which_key_flag else final
                        last_key_a = identity.copy() if which_key_flag else last_key_b.copy()
                        # this scale uses the calculated scale
                        last_key_b = identity.copy() if which_key_flag else last_key_delta.copy() + out * scale_pack
                        # if (trg_frame_i != out_frame_i) {
                        if next_key_offset:
                            # update scale_pack here, todo check if / what norm is used
                            # apparently also norm = 0 in acro_run, but too many to properly verify that for sucessive bones
                            scale_pack = self.get_pack_scale(mani_info)
                        segment_pos_bones[out_frame_i, pos_index] = final
                # print(segment_pos_bones[:, pos_index])
            else:
                # set all keyframes
                segment_pos_bones[:, pos_index] = vec[:3]
        logging.info(f"Segment[{i}] loc finished at bit {f.pos}, byte {f.pos / 8}")

    def printm(self, v):
        """print in order of memory register"""
        print(list(reversed(v)))

    def read_rot_keys(self, context, f, f2, i, k_channel_bitsize, mani_info, segment_frames_count,
                      segment_ori_bones, keys_iter=None):
        q_scale = 2 * math.pi  # 6.283185
        epsilon = 1.1920929E-7
        zeros = np.zeros(4, dtype=np.float32)
        identity = zeros.copy()
        identity[3] = 1.0
        scale = self.get_pack_scale(mani_info)
        for ori_index, ori_name in enumerate(mani_info.keys.ori_bones_names):
            # logging.info(context)
            frame_map = np.zeros(32, dtype=np.uint32)
            ushort_storage = np.zeros(156, dtype=np.uint32)
            # defines basic rot values
            # logging.info(f"ori[{ori_index}] {ori_name} at bit {f.pos}")
            f_pos = f.pos
            pos_base, vec = self.read_vec3(f)
            scale_pack = float(scale)
            # vec *= scale_pack * q_scale
            vec *= scale * q_scale
            norm = np.linalg.norm(vec)
            # logging.info(f"{ori_index} {ori_name} at {f_pos} {vec} {norm}")
            if norm < epsilon:
                quat = identity.copy()
            else:
                y_rel = identity.copy()
                y_rel[1] = vec[1] * vec[1]
                y_rel[0] = norm * 0.5
                b = identity.copy()
                b[1] = vec[2] * vec[2]
                b[0] = 0.0
                q, scale_fac = get_quat_scale_fac(norm * 0.5)
                # print(vec, norm)
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
            # logging.info(f"{(x, y, z)} {struct.pack('f', x), struct.pack('f', y), struct.pack('f', z)}")
            self.compare_key_with_reference(f, keys_iter, pos_base)
            # return
            # which channels are keyframed
            keys_flag = f.read_uint_reversed(3)
            keys_flag = StoreKeys.from_value(keys_flag)
            # logging.info(f"{keys_flag}")
            if keys_flag.x or keys_flag.y or keys_flag.z:
                wavelet_i, frame_map = self.read_wavelet_table(context, f2, frame_map, segment_frames_count)
                self.read_rel_keys(f, frame_map, k_channel_bitsize, keys_flag, ushort_storage, wavelet_i)
                # logging.info(f"key {i} = {rel_key_masked}")
                if segment_frames_count > 1:
                    frame_inc = 0
                    # print(ushort_storage)
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
                        #
                        # we're only accessing XYZ in code, but Q is set to 0.0 below so it's ok
                        rel = ushort_storage[out_frame_i*3: out_frame_i*3+4]
                        out = rel.astype(np.float32)
                        out[0] = self.make_signed(rel[0])
                        out[1] = self.make_signed(rel[1])
                        out[2] = self.make_signed(rel[2])
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
        logging.info(f"Segment[{i}] rot finished at bit {f.pos}, byte {f.pos / 8}")

    def get_pack_scale(self, mani_info, norm=0.000000000000000000000001):
        # the default initial scale seems to be for loc and rot
        # 1 / 16383 = 6.103888e-05
        # apparently starting out with norm=0
        # 0.00036623328924179077
        # print(norm)
        # xmm1 0 0 0 2730.5  # scale_f = 1 / norm
        # quantisation_level 420
        quant_fac = mani_info.keys.compressed.quantisation_level / norm
        # quant_fac in xmm3 0 0 0 1.14681e+006
        # quant_fac = 1146810.0
        quant_fac_clamped = np.clip(quant_fac, 128.0, 16383.0)
        # update the packed scale
        return 1 / quant_fac_clamped

    def read_rel_keys(self, f, frame_map, k_channel_bitsize, keys_flag, ushort_storage, wavelet_i):
        for channel_i, is_active in enumerate((keys_flag.z, keys_flag.y, keys_flag.x)):
            if is_active:
                # logging.info(f"rel_keys[{channel_i}] at bit {f.pos}")
                # define the minimal key size for this channel
                ch_key_size = f.read_uint_reversed(k_channel_bitsize + 1)
                ch_key_size_masked = ch_key_size & 0x1f
                assert ch_key_size <= 32
                # logging.info(f"channel[{channel_i}] base_size {ch_key_size} at bit {f.pos}")
                for trg_frame_i in frame_map[:wavelet_i]:
                    rel_key_flag = 1 << ch_key_size_masked | 1 >> (0x20 - ch_key_size_masked)
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
                    ushort_storage[channel_i + trg_frame_i * 3] = rel_key_masked

    def read_wavelet_table(self, context, f2, frame_map, segment_frames_count):
        # logging.info(f"wavelets at bit {f2.pos}")
        wavelet_i = 0
        for wave_frame_i in range(1, segment_frames_count):
            if context.i_in_run == 0:
                assert context.runs_remaining != 0
                context.runs_remaining -= 1
                context.do_increment = not context.do_increment
                init_k = context.init_k_a if context.do_increment else context.init_k_b
                assert init_k < 32
                # run 0: init_k_a = 2
                # run 1: init_k_b = 4
                # logging.info(f"do_increment {do_increment} init_k {init_k} at {f2.pos}")
                k_size = f2.read_bit_size_flag(32 - init_k)
                k_flag = 1 << (init_k & 0x1f)
                k_flag_out = f2.interpret_as_shift(k_size, k_flag)
                # logging.info(
                # 	f"pos before key {f2.pos}, k_flag_out {k_flag_out}, initk bare {k_size}")
                k_key = f2.read_uint_reversed(k_size + init_k)
                assert k_size + init_k < 32
                context.i_in_run = k_key + k_flag_out
            # logging.info(
            # 	f"wavelet_frame[{wave_frame_i}] total init_k {init_k + k_size} key {k_key} k_flag_out {k_flag_out} i {i_in_run}")
            # logging.info(f"pos after read {f2.pos}")
            context.i_in_run -= 1
            if context.do_increment:
                frame_map[wavelet_i] = wave_frame_i
                wavelet_i += 1

        # logging.info(frame_map)
        # logging.info(f"wavelets finished at bit {f2.pos}, byte {f2.pos / 8}, out_count {wavelet_i}")
        return wavelet_i, frame_map

    def read_vec3(self, f):
        # f_pos = int(f.pos)
        # pos_base = f.read_uint(45)
        pos_base = 0
        # # logging.info(f"{hex(pos_base)}, {pos_base}")
        # x = pos_base & 0x7fff
        # y = (pos_base >> 0xf) & 0x7fff
        # z = (pos_base >> 0x1e) & 0x7fff
        if self.context.version > 259:
            # current PZ, JWE2
            x = f.read_uint(15)
            y = f.read_uint(15)
            z = f.read_uint(15)
        else:
            # PC, JWE1, old PC have the order reversed
            x = f.read_uint_reversed(15)
            y = f.read_uint_reversed(15)
            z = f.read_uint_reversed(15)
        raw = np.zeros(4, dtype=np.uint32)
        raw[:3] = x, y, z
        vec = np.zeros(4, dtype=np.float32)
        vec[0] = self.make_signed(x)
        vec[1] = self.make_signed(y)
        vec[2] = self.make_signed(z)
        # print(x,vec[0])
        # logging.info(f"{(x, y, z)} {(hex(x), hex(y), hex(z))}")
        return pos_base, vec

    def compare_key_with_reference(self, f, keys_iter, pos_base):
        if keys_iter is not None:
            expected_key = next(keys_iter)
            expected_key_bin = bitarray.util.int2ba(expected_key, length=45, endian="little", signed=False)
            f.find_all(expected_key_bin)
            # logging.info(f"Expected {expected_key} found at bits {tuple(f.find_all(expected_key_bin))}")
            if expected_key != pos_base:
                raise AttributeError(f"Expected and found keys do not match")

    def make_signed(self, x):
        return -(x + 1 >> 1) if x & 1 else x >> 1


if __name__ == "__main__":
    logging_setup("mani")
    # for k in (0, 1, 4, 5, 6, 32, 34, 36, 37, 38, 64, 66, 68, 69, 70, 82):
    #     print(ManisDtype.from_value(k))
    # print(bin(-4395513102365351936))
    # print(bin(554058852231815168))
    # key = Key94C.from_value(2305843010808512512)
    # key.type = 0
    # key.loc_x = 0
    # key.loc_y = 0
    # # key.loc_z = 0b11111111111111111111
    # key.loc_z = 0b11111111111111111111
    # # key.unk = 0
    # # key.more_loc = 0
    # key.rot_rel = 4
    # print(key)
    mani = ManisFile()
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
    # mani.show_floats("Track")

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

    # mani.load("C:/Users/arnfi/Desktop/acro/motionextracted.maniset85c65403.manis")  # locomotion
    # # mani.parse_keys("acrocanthosaurus@run")
    # # todo see if def_horselink_joint_IKBlend.L loc can be easily debugged
    # mani.parse_keys("acrocanthosaurus@walk")
    # # mani.show_floats("phase")

    # # JWE1
    mani.load("C:/Users/arnfi/Desktop/anky_JWE1/fighting.maniset2b08396d.manis")  # fighting
    print(mani)
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
# hex_test()

