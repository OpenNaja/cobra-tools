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


class BaniFile(BaniInfo, IoFile):

	def __init__(self):
		super().__init__(BaniContext())
		# the output array
		self.bones_frames_eulers = []
		self.bones_frames_locs = []
		# input
		self.keys = []
		self.banis = BanisFile()

	def load(self, filepath):
		# store file name for later
		self.file = filepath
		self.dir, self.basename = os.path.split(filepath)
		self.path_no_ext = os.path.splitext(self.file)[0]
		with open(filepath, "rb") as stream:
			self.read_fields(stream, self)

	def read_banis(self, ):
		# get banis file
		banis_path = os.path.join(self.dir, self.banis_name)
		self.banis.load(banis_path)

	# self.decode_keys()

	@property
	def eulers(self):
		return self.banis.data["euler"][self.data.read_start_frame:self.data.read_start_frame + self.data.num_frames, :]

	@property
	def locs(self):
		return self.banis.data["loc"][self.data.read_start_frame:self.data.read_start_frame + self.data.num_frames, :]

	def encode_eulers(self, ):
		# todo: update array size

		eulers = [self.eulers_dict[bone_name] for bone_name in self.names]
		# print(eulers)
		# print(list(zip(eulers)))
		num_bones = len(self.names)
		num_frames = len(eulers[0])
		for bone_i in range(num_bones):
			for frame_i in range(num_frames):
				in_key = eulers[bone_i][frame_i]
				out_key = self.keys[frame_i][bone_i]
		# todo: actually store the exported value
		# print(export_key(in_key), out_key)

	def save(self, filepath):
		# write the file
		# todo - this is not properly implemented
		self.encode_eulers()
		with open(filepath, "wb") as stream:
			self.write_fields(stream, self)
	# got to write the banis too


class BanisFile(BanisInfoHeader, IoFile):

	def __init__(self):
		super().__init__(BaniContext())
		self.data = None

	def load(self, filepath):
		# store file name for later
		self.file = filepath
		self.dir, self.basename = os.path.split(filepath)
		self.path_no_ext = os.path.splitext(self.file)[0]

		with open(filepath, "rb") as stream:
			self.read_fields(stream, self)
			dt = np.dtype([
				("euler", np.short, (3,)),
				("loc", np.ushort, (3,)),
			])
			self.data = np.empty(dtype=dt, shape=(self.num_frames, self.num_bones))
			stream.readinto(self.data)
			ft = np.dtype([
				("euler", np.float32, (3,)),
				("loc", np.float32, (3,)),
			])
			self.data = self.data.astype(ft)
			print(self.data[0, :, ])
			self.data["euler"] = self.data["euler"] / 32767.0 * 180
			# self.data["euler"] = self.data["euler"] / 32768.0 * 180 + 90.0
			self.data["euler"][:, :, 0] += 90.0
			self.data["euler"][:, :, 1] += 90.0
			self.data["euler"][:, :, 2] -= 90.0
			# [[[89.9945  1.0162 89.9945]
			#   [89.978  -2.7026 90.5548]
			#   [89.978  -2.7026 90.5548]

			# for frame_i in range(self.num_frames):
			# 	for bone_i in range(self.num_bones):
			# 		e = self.data["euler"][frame_i, bone_i]
			# 		# this is irreversible, fixing gimbal issues in baked anims; game fixes these as well and does not mind our fix
			# 		if frame_i:
			# 			# get previous euler for this bone
			# 			last_euler = self.data["euler"][frame_i - 1, bone_i]
			# 			for key_i in range(3):
			# 				# found weird axis cross, correct for it
			# 				if abs(e[key_i] - last_euler[key_i]) > 45.0:
			# 					e[key_i] = math.copysign((180.0 - e[key_i]), last_euler[key_i])
			# 			self.data["euler"][frame_i, bone_i] = e

			# from tuna appears to be without loc_min_rel
			fac = 2.0  # JWE2 tuna
			# no 2.0 scale here, but maybe self.loc_min_rel plays into this?
			if "food_carnivore" in self.file:
				fac = 1.0
			self.data["loc"] = (self.data["loc"] - 32767.0) * self.loc_scale * fac  # + self.loc_min_rel
		loc_min_rel = np.min(self.data["loc"]) / fac
		# print(self.data["euler"])
		print(self.data[0, :, ])
		print(loc_min_rel)
		# for tuna, self.loc_min_rel = np.min(self.data["loc"]) / 2
		# self.data["loc"] += self.loc_min_rel
		print(self)

	def save(self, filepath):
		self.num_frames, self.num_bones = self.data.shape
		with open(filepath, "wb") as stream:
			self.write_fields(stream, self)
			stream.write(self.data.tobytes())

	# def rebuild_buffer(self, bani_files):
	# 	for bani in bani_files:
	# 		assert bani.data.


if __name__ == "__main__":
	banis = BanisFile()
	# banis.load("C:/Users/arnfi/Desktop/gila/gila_monster_idles.banisetc1b711e6 - just one anim.banis")
	# # i = np.interp()
	# x = np.linspace(-np.pi, np.pi, banis.num_frames)
	# # sin_dat = (np.sin(x)+1)*32768
	# sin_dat = np.sin(x) * 25000 + 32768
	# banis.data[:, 7]["loc"][:, 2] = sin_dat
	# # sin2_dat = (np.sin(x)+1)*32768  # for ushort
	# sin2_dat = np.sin(x) * 2000 - 10834
	# # print(sin2_dat)
	#
	# # it does not appear to be the normalized remainder of a quat
	# # for bone in range(banis.num_bones):
	# # 	print(bone)
	# # 	for x, y, z in banis.data[:, bone]["euler"].astype(dtype=np.float32):
	# # 		print(bone, math.sqrt(x*x+y*y+z*z))
	# # banis.data[:, 7]["euler"][:, 0] = 0
	# # banis.data[:, 7]["euler"][:, 2] = 32768
	# # banis.data[:, 7]["euler"][:, 2] = sin2_dat
	# # 0 = rotate about global X in blender
	# # 1 = rotate about global Z in blender
	# # 2 = rotate about global Y in blender
	# head_keys = banis.data[:, 7]["euler"][:, 2]
	# banis.save("C:/Users/arnfi/Desktop/gila/gila_monster_idles.banisetc1b711e6.banis")
	# banis.load("C:/Users/arnfi/Desktop/Coding/Frontier/anim/banis/food/food_carnivore.banisetfcbde7ca.banis")
	banis.load("C:/Users/arnfi/Desktop/Coding/Frontier/anim/banis/food/food_carnivore.banisetfcbde7ca.banis")
	# print(head_keys)
