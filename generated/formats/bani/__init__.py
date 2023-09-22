from generated.formats.bani.imports import name_type_map
from generated.formats.bani.compounds.BaniInfo import BaniInfo
from generated.formats.bani.compounds.BanisInfoHeader import BanisInfoHeader
from generated.formats.bani.compounds.BanisRoot import BanisRoot
from generated.io import IoFile
import os

import math
import numpy as np


def export_key(key):
	# this seems to be a modulo equivalent
	k = [x for x in key]
	for i in range(3):
		# if k[i] < -180:
		# k[i]+= 360
		if k[i] < -90:
			k[i] = 360 - k[i]
	k[0] -= 90
	k[2] += 90
	# calculate short
	k = [int(x / 180 * 32768 - 16385) for x in k]
	return k


class BaniContext(object):
	def __init__(self):
		self.version = 0
		self.user_version = 0

	def __repr__(self):
		return f"{self.version} | {self.user_version}"


class BanisFile(BanisInfoHeader, IoFile):
	dt = np.dtype([
		("euler", np.short, (3,)),
		("loc", np.ushort, (3,)),
	])
	ft = np.dtype([
		("euler", np.float32, (3,)),
		("loc", np.float32, (3,)),
	])

	def __init__(self):
		super().__init__(BaniContext())
		self.keys = None

	def load(self, filepath):
		# store file name for later
		self.file = filepath
		self.dir, self.basename = os.path.split(filepath)
		self.path_no_ext = os.path.splitext(self.file)[0]

		with open(filepath, "rb") as stream:
			self.read_fields(stream, self)
			raw_keys = np.empty(dtype=self.dt, shape=(self.data.num_frames, self.data.num_bones))
			stream.readinto(raw_keys)
			self.keys = raw_keys.astype(self.ft)
			print(raw_keys[0, :, ])
			self.keys["euler"] = self.keys["euler"] / 32767.0 * 180
			# self.keys["euler"] = self.keys["euler"] / 32768.0 * 180 + 90.0
			self.keys["euler"][:, :, 0] += 90.0
			self.keys["euler"][:, :, 1] += 90.0
			self.keys["euler"][:, :, 2] -= 90.0
			# [[[89.9945  1.0162 89.9945]
			#   [89.978  -2.7026 90.5548]
			#   [89.978  -2.7026 90.5548]

			self.keys["loc"] = self.keys["loc"] * self.data.loc_scale + self.data.loc_min
		# print(self.keys["euler"])
		print(self.keys[0, :, ])
		print(self)
		for bani in self.anims:
			bani.keys = self.keys[bani.data.read_start_frame: bani.data.read_start_frame + bani.data.num_frames]

	def save(self, filepath):
		self.num_anims = len(self.anims)
		offset = 0
		self.data.num_frames = 0
		for bani in self.anims:
			bani.data.num_frames = len(bani.keys)
			self.data.num_frames += bani.data.num_frames
			bani.data.read_start_frame = offset
			offset += bani.data.num_frames
		# assume all have same bone count
		_num_frames, self.data.num_bones = bani.keys.shape
		self.data.bytes_per_frame = 12
		self.data.bytes_per_bone = self.data.num_bones * self.data.bytes_per_frame
		# reassemble the whole array as floats
		float_keys = np.empty(dtype=self.ft, shape=(self.data.num_frames, self.data.num_bones))
		for bani in self.anims:
			float_keys[bani.data.read_start_frame: bani.data.read_start_frame + bani.data.num_frames] = bani.keys

		# cf https://nfrechette.github.io/2016/11/09/anim_compression_range_reduction/
		# choose loc scale to spread loc range across 0 - 65535
		# todo - make 0.0 land on 32767.0, seems to be that way in stock
		self.data.loc_min = np.min(float_keys["loc"])
		self.data.loc_scale = (np.max(float_keys["loc"]) - self.data.loc_min) / 65535
		float_keys["loc"] = (float_keys["loc"] - self.data.loc_min) / self.data.loc_scale

		float_keys["euler"][:, :, 0] -= 90.0
		float_keys["euler"][:, :, 1] -= 90.0
		float_keys["euler"][:, :, 2] += 90.0
		float_keys["euler"] = float_keys["euler"] * 32767.0 / 180
		# round parts separately
		float_keys["euler"].round(out=float_keys["euler"])
		float_keys["loc"].round(out=float_keys["loc"])
		# pack to short
		raw_keys = float_keys.astype(self.dt)
		print(raw_keys[0, :, ])
		with open(filepath, "wb") as stream:
			self.write_fields(stream, self)
			stream.write(raw_keys.tobytes())
		print(self.data)


if __name__ == "__main__":
	banis = BanisFile()
	# banis.load("C:/Users/arnfi/Desktop/gila/gila_monster_idles.banisetc1b711e6 - just one anim.banis")
	# # i = np.interp()
	# x = np.linspace(-np.pi, np.pi, banis.num_frames)
	# # sin_dat = (np.sin(x)+1)*32768
	# sin_dat = np.sin(x) * 25000 + 32768
	# banis.keys[:, 7]["loc"][:, 2] = sin_dat
	# # sin2_dat = (np.sin(x)+1)*32768  # for ushort
	# sin2_dat = np.sin(x) * 2000 - 10834
	# # print(sin2_dat)
	#
	# # it does not appear to be the normalized remainder of a quat
	# # for bone in range(banis.num_bones):
	# # 	print(bone)
	# # 	for x, y, z in banis.keys[:, bone]["euler"].astype(dtype=np.float32):
	# # 		print(bone, math.sqrt(x*x+y*y+z*z))
	# # banis.keys[:, 7]["euler"][:, 0] = 0
	# # banis.keys[:, 7]["euler"][:, 2] = 32768
	# # banis.keys[:, 7]["euler"][:, 2] = sin2_dat
	# # 0 = rotate about global X in blender
	# # 1 = rotate about global Z in blender
	# # 2 = rotate about global Y in blender
	# head_keys = banis.keys[:, 7]["euler"][:, 2]
	# banis.save("C:/Users/arnfi/Desktop/gila/gila_monster_idles.banisetc1b711e6.banis")
	# banis.load("C:/Users/arnfi/Desktop/Coding/Frontier/anim/banis/food/food_carnivore.banisetfcbde7ca.banis")
	banis.load("C:/Users/arnfi/Desktop/food_carnivore.banisetfcbde7ca.banis")
	banis.save("C:/Users/arnfi/Desktop/food_carnivore.banisetfcbde7ca_test.banis")
	# print(head_keys)
