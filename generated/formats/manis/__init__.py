from generated.formats.manis.imports import name_type_map
import io
import logging
import struct

import root_path
from generated.formats.base.basic import Ushort
from generated.formats.manis.bitfields.ChannelSize import ChannelSize
from generated.formats.manis.bitfields.Key94 import Key94
from generated.formats.manis.bitfields.Key94B import Key94B
from generated.formats.manis.bitfields.Key94C import Key94C
from generated.formats.manis.bitfields.ManisDtype import ManisDtype
from generated.formats.manis.bitfields.PosBaseKey import PosBaseKey
from generated.formats.manis.bitfields.PosFrameInfo import PosFrameInfo
from generated.formats.manis.bitfields.SegmentInfo import SegmentInfo
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
		d = self.data[self.pos: self.pos+size]
		self.pos += size
		return d

	def read_int(self, size):
		bits = self.read(size)
		return bitarray.util.ba2int(bits, signed=False)
		# return bitarray.util.int2ba(0x99c51a50c66, length=45, endian="little", signed=False)

	def read_int_reversed(self, size):
		out = 0
		for _ in range(size):
			new_bit = self.read_int(1)
			out = new_bit | out * 2
		return out

	def read_bit_size_flag(self, max_size):
		for rel_key_size in range(max_size):
			new_bit = self.read_int(1)
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
		return min(32, frame_count - (i*32))

	def parse_keys(self):
		k_channel_bitsize = self.get_bitsize()
		run_rel_i = 0
		logging.info(f"k_channel_bitsize {k_channel_bitsize}")
		dump_path = os.path.join(root_path.root_dir, "dumps", "jmp2.bin")
		with open(dump_path, "rb") as jmp1:
			jmp1_stream = BinStream(jmp1.read())
		for mani_info in self.iter_compressed_manis():
			if mani_info.name != "acrocanthosaurus@standidle01":
				continue
			# acro debug keys
			dump_path = os.path.join(root_path.root_dir, "dumps", "acro_keys.txt")
			keys = [int(line.strip(), 0) for line in open(dump_path, "r")]
			keys_iter = iter(keys)
			# key_i =
			logging.info(f"Anim {mani_info.name} with {len(mani_info.keys.compressed.segments)} segments, {mani_info.frame_count} frames")
			for i, mb in enumerate(mani_info.keys.compressed.segments):
				try:
					segment_frames_count = self.segment_frame_count(i, mani_info.frame_count)  # - 1
					logging.info(f"Segment[{i}] frames {segment_frames_count}")
					f = BinStream(mb.data)
					f2 = BinStream(mb.data)
					# k = bitarray.util.int2ba(4040, length=16, endian="big", signed=False)
					# print(k)
					# f.find_all(k)
					# print(keys)
					# this is a jump to the end of the compressed keys
					num_bytes = f.read_int_reversed(16)
					logging.info(f"num_bytes {num_bytes}")

					# anim_decompression_read_wavelet
					f2.seek(num_bytes * 8)
					flag_0 = f2.read_int(1)
					runs_remaining = f2.read_int(16)
					init_k = f2.read_int_reversed(k_channel_bitsize)
					output_b = f2.read_int_reversed(k_channel_bitsize)
					print(flag_0, runs_remaining, init_k, output_b)
					frame_map = {}
					# return
					assert mani_info.keys.compressed.pos_bone_count == mani_info.pos_bone_count
					for pos_index, pos_name in enumerate(mani_info.keys.pos_bones_names):
						# definitely not byte aligned as the key bytes can not be found in the manis data
						# defines basic loc values and which channels are keyframed
						logging.info(f"pos[{pos_index}] {pos_name} at bit {f.pos}")
						pos_base = f.read_int(45)
						keys_flag = f.read_int_reversed(3)
						# logging.info(pos_base)
						pos_base = PosBaseKey.from_value(pos_base)
						keys_flag = StoreKeys.from_value(keys_flag)
						logging.info(f"{pos_base} {keys_flag}")
						expected_key = next(keys_iter)
						expected_key_bin = bitarray.util.int2ba(expected_key, length=45, endian="little", signed=False)
						# f.find_all(expected_key_bin)
						logging.info(f"Expected {expected_key} found at bits {tuple(f.find_all(expected_key_bin))}")
						if expected_key != pos_base:
							logging.warning(f"Expected and found keys do not match")
							return
						# return
						if keys_flag.x or keys_flag.y or keys_flag.z:
							logging.info(f"wavelet at bit {f2.pos}")
							wavelet_i = 0
							for wave_frame_i in range(segment_frames_count):
								if run_rel_i == 0:
									assert runs_remaining != 0
									runs_remaining -= 1
									flag_0 = True
									assert init_k < 32
									k_size = f2.read_bit_size_flag(32)
									k_key = f2.read_int_reversed(k_size + init_k)
									# todo set run_rel_i correctly
									run_rel_i = k_key  # + shifted flag
									logging.info(f"wavelet_frame[{wave_frame_i}] {init_k} {k_size} {k_key}")
									logging.info(f"wavelet finished at bit {f2.pos}, byte {f2.pos / 8}")
								run_rel_i -= 1
								# seems to always pass
								if flag_0:
									wavelet_i += 1
									frame_map[wavelet_i] = wave_frame_i

							for channel_i, is_active in enumerate((keys_flag.x, keys_flag.y, keys_flag.z)):
								if is_active:

									logging.info(f"rel_keys[{channel_i}] at bit {f.pos}")
									# define the minimal key size for this channel
									ch_key_size = f.read_int_reversed(k_channel_bitsize)
									ch_key_size_masked = ch_key_size & 0x1f
									logging.info(f"channel[{channel_i}] base_size {ch_key_size}")
									# channel_val = PosFrameInfo.from_value(channel_val)
									for frame_i in range(wavelet_i):
										rel_key_flag = 1 << ch_key_size_masked | 1 >> 0x20 - ch_key_size_masked
										channel_bitsize = 0
										# get additional key size for this key
										for rel_key_size in range(16):
											new_bit_flag = f.read_int(1)
											channel_bitsize += rel_key_flag
											rel_key_flag *= 2
											if not new_bit_flag:
												break
										ch_rel_key_size = ch_key_size + rel_key_size
										# ensure the final key size is valid
										assert ch_rel_key_size <= 32
										logging.info(f"ch_rel_key_size {ch_rel_key_size}")
										# read the key, if it has a size
										if ch_rel_key_size:
											ch_rel_key = f.read_int_reversed(ch_rel_key_size)
										else:
											ch_rel_key = 0
										# logging.info(f"key = {ch_rel_key}")
									# logging.info(f"{rel_key_size}, {channel_bitsize}, {frames_flag}, {frames_flag_2}")

									# break
						else:
							pass
							# set all keyframes
					logging.info(f"loc finished at bit {f.pos}, byte {f.pos/8}")
					break
				except bitstring.ReadError:
					logging.exception(f"Reading failed at bit {f.pos}, byte {f.pos/8}")


if __name__ == "__main__":
	logging_setup("mani")
	# for k in (0, 1, 4, 5, 6, 32, 34, 36, 37, 38, 64, 66, 68, 69, 70):
	# 	print(ManisDtype.from_value(k))
	# print(bin(-4395513102365351936))
	# print(bin(554058852231815168))
	key = Key94C.from_value(2305843010808512512)
	key.type = 0
	key.loc_x = 0
	key.loc_y = 0
	# key.loc_z = 0b11111111111111111111
	key.loc_z = 0b11111111111111111111
	# key.unk = 0
	# key.more_loc = 0
	key.rot_rel = 4
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