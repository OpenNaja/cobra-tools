import io
import logging
import struct

import numpy as np

import root_path
from generated.formats.manis.bitfields.ManisDtype import ManisDtype
from generated.formats.manis.bitfields.PosBaseKey import PosBaseKey
from generated.formats.manis.bitfields.StoreKeys import StoreKeys
from generated.formats.manis.compounds.InfoHeader import InfoHeader
from generated.io import IoFile
import os

from modules.formats.shared import get_padding_size
from ovl_util.config import logging_setup

try:
	import bitstring
	import bitarray
	import bitarray.util
except:
	logging.warning(f"bitstring module is not installed")


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

	def read_int_reversed(self, size):
		out = 0
		for _ in range(size):
			new_bit = self.read_uint(1)
			out = new_bit | (out * 2)
		return out

	def read_as_shift(self, size, flag):
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
			for mi, name in zip(self.mani_infos, self.names):
				mi.name = name
				if hasattr(mi, "keys"):
					mi.keys.name = name
					mi.keys.compressed.name = name
				# print(mi.keys.name)
				# if mi.root_pos_bone != 255:
				# 	print(mi.root_pos_bone, mi.keys.pos_bones_names[mi.root_pos_bone])
				# if mi.root_ori_bone != 255:
				# 	print(mi.root_ori_bone, mi.keys.ori_bones_names[mi.root_ori_bone])

	def iter_compressed_manis(self):
		for mani_info in self.mani_infos:
			if hasattr(mani_info, "keys"):
				if hasattr(mani_info.keys.compressed, "segments"):
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
		new_bit = 0xf  # MOV new_bit,0xf
		# return new_bit.bit_length()  # - 1
		return new_bit.bit_length() - 1

	# for i in reversed(range(31, -1, -1)):
	# 	# print(i, 15 >> i)
	# 	if 15 >> i == 0:
	# 		return i
	# return -1

	def segment_frame_count(self, i, frame_count):
		# get from chunk index
		return min(32, frame_count - (i * 32))

	def parse_keys(self):
		scale = 6.103888e-05
		k_channel_bitsize = self.get_bitsize()
		logging.info(f"k_channel_bitsize {k_channel_bitsize}")
		for mani_info in self.iter_compressed_manis():
			if mani_info.name != "acrocanthosaurus@standidle01":
				continue
			# acro debug keys
			dump_path = os.path.join(root_path.root_dir, "dumps", "acro_keys.txt")
			keys = [int(line.strip(), 0) for line in open(dump_path, "r")]
			keys_iter = iter(keys)
			logging.info(
				f"Anim {mani_info.name} with {len(mani_info.keys.compressed.segments)} segments, {mani_info.frame_count} frames")
			mani_info.keys.compressed.pos_bones = np.empty((mani_info.frame_count, mani_info.pos_bone_count, 3), np.float32)
			assert mani_info.keys.compressed.pos_bone_count == mani_info.pos_bone_count
			frame_offset = 0
			for i, mb in enumerate(mani_info.keys.compressed.segments):
				try:
					i_in_run = 0
					segment_frames_count = self.segment_frame_count(i, mani_info.frame_count)  # - 1
					segment_pos_bones = mani_info.keys.compressed.pos_bones[frame_offset:frame_offset+segment_frames_count]
					logging.info(f"Segment[{i}] frames {segment_frames_count}, shape {segment_pos_bones.shape}")
					f = BinStream(mb.data)
					f2 = BinStream(mb.data)

					# this is a jump to the end of the compressed keys
					num_bytes = f.read_int_reversed(16)
					logging.info(f"num_bytes {num_bytes}")
					do_increment, init_k_a, init_k_b, runs_remaining = self.read_wavelet(f2, num_bytes)
					begun = True
					for pos_index, pos_name in enumerate(mani_info.keys.pos_bones_names):
						frame_map = np.zeros(32, dtype=np.uint32)
						ushort_storage = np.zeros(156, dtype=np.uint32)
						# definitely not byte aligned as the key bytes can not be found in the manis data
						# defines basic loc values and which channels are keyframed
						logging.info(f"pos[{pos_index}] {pos_name} at bit {f.pos}")
						f_pos = f.pos
						pos_base = f.read_uint(45)
						# logging.info(pos_base)
						logging.info(f"{hex(pos_base)}, {pos_base}")
						x = pos_base & 0x7fff
						y = (pos_base >> 0xf) & 0x7fff
						z = (pos_base >> 0x1e) & 0x7fff
						x = self.make_signed(x)
						y = self.make_signed(y)
						z = self.make_signed(z)
						# (0.093084292, 0.17859976288, 0.0848440432)
						# (0.20734907536, 0.27565158208, -0.30037232848)
						# f.pos = f_pos
						# x = f.read_int(15)
						# y = f.read_int(15)
						# z = f.read_int(15)
						# logging.info(f"{(x, y, z)} {(hex(x), hex(y), hex(z))}")
						x *= scale
						y *= scale
						z *= scale
						# logging.info(f"{(x, y, z)} {struct.pack('f', x), struct.pack('f', y), struct.pack('f', z)}")
						expected_key = next(keys_iter)
						expected_key_bin = bitarray.util.int2ba(expected_key, length=45, endian="little", signed=False)
						f.find_all(expected_key_bin)
						logging.info(f"Expected {expected_key} found at bits {tuple(f.find_all(expected_key_bin))}")
						if expected_key != pos_base:
							logging.warning(f"Expected and found keys do not match")
							return
						# return
						keys_flag = f.read_int_reversed(3)
						keys_flag = StoreKeys.from_value(keys_flag)
						logging.info(f"{keys_flag}")
						if keys_flag.x or keys_flag.y or keys_flag.z:
							# logging.info(f"wavelets at bit {f2.pos}")
							wavelet_i = 0
							for wave_frame_i in range(1, segment_frames_count):
								if i_in_run == 0:
									assert runs_remaining != 0
									runs_remaining -= 1
									do_increment = not do_increment
									init_k = init_k_a if do_increment else init_k_b
									assert init_k < 32
									# run 0: init_k_a = 2
									# run 1: init_k_b = 4
									logging.info(f"do_increment {do_increment} init_k {init_k} at {f2.pos}")
									k_size = f2.read_bit_size_flag(32 - init_k)
									k_flag = 1 << (init_k & 0x1f)
									k_flag_out = f2.read_as_shift(k_size, k_flag)
									# logging.info(
									# 	f"pos before key {f2.pos}, k_flag_out {k_flag_out}, initk bare {k_size}")
									k_key = f2.read_int_reversed(k_size + init_k)
									assert k_size + init_k < 32
									i_in_run = k_key + k_flag_out
									# logging.info(
									# 	f"wavelet_frame[{wave_frame_i}] total init_k {init_k + k_size} key {k_key} k_flag_out {k_flag_out} i {i_in_run}")
									logging.info(f"pos after read {f2.pos}")
								i_in_run -= 1
								if do_increment:
									frame_map[wavelet_i] = wave_frame_i
									wavelet_i += 1
							logging.info(frame_map)
							logging.info(f"wavelets finished at bit {f2.pos}, byte {f2.pos / 8}, out_count {wavelet_i}")
							for channel_i, is_active in enumerate((keys_flag.x, keys_flag.y, keys_flag.z)):
								if is_active:

									# logging.info(f"rel_keys[{channel_i}] at bit {f.pos}")
									# define the minimal key size for this channel
									ch_key_size = f.read_int_reversed(k_channel_bitsize + 1)
									ch_key_size_masked = ch_key_size & 0x1f
									assert ch_key_size <= 32
									# logging.info(f"channel[{channel_i}] base_size {ch_key_size}")
									# channel_val = PosFrameInfo.from_value(channel_val)
									for trg_frame_i in frame_map[:wavelet_i]:
										rel_key_flag = 1 << ch_key_size_masked | 1 >> 0x20 - ch_key_size_masked
										rel_key_size = f.read_bit_size_flag(32 - ch_key_size_masked)
										rel_key_base = f.read_as_shift(rel_key_size, rel_key_flag)
										ch_rel_key_size = ch_key_size + rel_key_size
										# ensure the final key size is valid
										assert ch_rel_key_size <= 32
										# logging.info(f"ch_rel_key_size {ch_rel_key_size}")
										# read the key, if it has a size
										if ch_rel_key_size:
											ch_rel_key = f.read_int_reversed(ch_rel_key_size)
										else:
											ch_rel_key = 0
										# logging.info(f"key = {ch_rel_key}")
										rel_key_masked = (rel_key_base + ch_rel_key) & 0xffff
										ushort_storage[channel_i + trg_frame_i*3] = rel_key_masked
									# ushort_storage for acro's first use
									# 000000773047FA50      0     0     0     8    61     0     5    60
									# 000000773047FA60      8     3     0     9     0     8     0     8
									# 000000773047FA70      9     4     9     0     0     6    12     5
									# 000000773047FA80      0     9     4     7     0     0     8     6
									# 000000773047FA90      0     0     3     0     5     0     4     4
									# 000000773047FAA0      0     5     0     6     0     0     7     0
									# 000000773047FAB0      0     6     6     0     0     3     5     5
									# 000000773047FAC0      0     6     4     5     0     0    10     0
									# 000000773047FAD0      4     5     0     3     0     0     0     8
									# 000000773047FAE0      0     0     9     5     0     4     8     0
									# 000000773047FAF0      0     0     6     0     5     7     0     6
									# 000000773047FB00      4     3     0     0     6     7     0     0
									# 000000773047FB10      0     0     0     0     0     0     0     0
									# 000000773047FB20      0     0     0     0     0     0     0     0
									# 000000773047FB30      0     0     0     0     0     0     0     0
									# logging.info(f"key {i} = {rel_key_masked}")
							if segment_frames_count > 1:
								frame_inc = 0
								# print(ushort_storage)
								# set base keyframe
								segment_pos_bones[0, pos_index, 0] = x
								segment_pos_bones[0, pos_index, 1] = y
								segment_pos_bones[0, pos_index, 2] = z
								# set other keyframes
								for out_frame_i in range(1, segment_frames_count):
									trg_frame_i = frame_map[frame_inc]
									if trg_frame_i == out_frame_i:
										frame_inc += 1
									rel_x = ushort_storage[out_frame_i*3]
									rel_y = ushort_storage[out_frame_i*3+1]
									rel_z = ushort_storage[out_frame_i*3+2]
									rel_x = self.make_signed(rel_x)
									rel_y = self.make_signed(rel_y)
									rel_z = self.make_signed(rel_z)
									rel_x *= scale
									rel_y *= scale
									rel_z *= scale
									final_x = x + rel_x
									final_y = y + rel_y
									final_z = z + rel_z
									# print(rel_x, rel_y, rel_z)
									# print(final_x, final_y, final_z)
									segment_pos_bones[out_frame_i, pos_index, 0] = final_x
									segment_pos_bones[out_frame_i, pos_index, 1] = final_y
									segment_pos_bones[out_frame_i, pos_index, 2] = final_z
									# return
								# break
						else:
							# set all keyframes
							segment_pos_bones[:, pos_index, 0] = x
							segment_pos_bones[:, pos_index, 1] = y
							segment_pos_bones[:, pos_index, 2] = z
					logging.info(f"Segment[{i}] loc finished at bit {f.pos}, byte {f.pos / 8}")
					# break
				except:
					logging.exception(f"Reading Segment[{i}] failed at bit {f.pos}, byte {f.pos / 8}")
					raise
				# rot
				for _ in range(mani_info.ori_bone_count):
					ori_key = next(keys_iter)
				frame_offset += segment_frames_count
			print(mani_info.keys.compressed.pos_bones)

	def read_wavelet(self, f2, num_bytes):
		f2.seek(num_bytes * 8)
		do_increment = f2.read_uint(1)
		runs_remaining = f2.read_uint(16)
		# size = k_channel_bitsize + 1
		# verified
		size = 4
		init_k_a = f2.read_int_reversed(size)
		init_k_b = f2.read_int_reversed(size)
		if not do_increment:
			init_k_a, init_k_b = init_k_b, init_k_a
		logging.info(
			f"do_increment {do_increment}, runs_remaining {runs_remaining}, init_k_a {init_k_a}, init_k_b {init_k_b}")
		do_increment = not do_increment
		return do_increment, init_k_a, init_k_b, runs_remaining

	def make_signed(self, x):
		return -(x + 1 >> 1) if x & 1 else x >> 1


if __name__ == "__main__":
	logging_setup("mani")
	# for k in (0, 1, 4, 5, 6, 32, 34, 36, 37, 38, 64, 66, 68, 69, 70):
	# 	print(ManisDtype.from_value(k))
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
	# acro stand_ide
	target = "acrocanthosaurus@standidle01"
	mani.load("C:/Users/arnfi/Desktop/acro/notmotionextracted.maniset53978456.manis")
	# mani.load("C:/Users/arnfi/Desktop/animationmotionextractedlocomotion.maniset648a1a01.manis")
	# mani.load("C:/Users/arnfi/Desktop/crane/animationnotmotionextractedfighting.maniset3d816f2c.manis")
	# mani.load("C:/Users/arnfi/Desktop/kangaroo/animation.maniset32dc487b.manis")
	# mani.load("C:/Users/arnfi/Desktop/Wheel/animation.maniset9637aeb4.manis")
	# mani.load("C:/Users/arnfi/Desktop/DLA scale anim.manis")
	# mani.load("C:/Users/arnfi/Desktop/dinomascot/animation.maniset293c241f.manis")
	# mani.dump_keys()
	mani.parse_keys()
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
