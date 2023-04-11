from generated.formats.bani.imports import name_type_map
from generated.formats.bani.compounds.BaniInfoHeader import BaniInfoHeader
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
	k[0]-=90
	k[2]+=90
	# calculate short
	k = [int(x/180*32768-16385) for x in k]
	return k


class BaniContext(object):
	def __init__(self):
		self.version = 0
		self.user_version = 0

	def __repr__(self):
		return f"{self.version} | {self.user_version}"


class BaniFile(BaniInfoHeader, IoFile):

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
		self.decode_keys()

	def decode_keys(self):

		# create function for doing interpolation of the desired ranges
		# center = self.banis.loc_center
		# first = self.banis.translation_first
		self.eulers = np.empty((self.data.num_frames, self.banis.num_bones, 3), dtype=np.float32)
		self.locs = np.empty((self.data.num_frames, self.banis.num_bones, 3), dtype=np.float32)
		ft = np.dtype([
			("euler", np.float32, (3,)),
			("loc", np.float32, (3,)),
		])
		data = self.banis.data.astype(ft)
		# convert to floats
		for frame_i in range(self.data.num_frames):
			for bone_i in range(self.banis.num_bones):
				e = data[self.data.read_start_frame+frame_i, bone_i]["euler"]
				e = (e + 16385) * 180 / 32768
				e[0] += 90
				e[2] -= 90
				# this is irreversible, fixing gimbal issues in baked anims; game fixes these as well and does not mind our fix
				if frame_i:
					# get previous euler for this bone
					last_euler = self.eulers[frame_i - 1, bone_i]
					for key_i in range(3):
						# found weird axis cross, correct for it
						if abs(e[key_i] - last_euler[key_i]) > 45:
							e[key_i] = math.copysign((180 - e[key_i]), last_euler[key_i])
				self.eulers[frame_i, bone_i] = e

				l = data[self.data.read_start_frame+frame_i, bone_i]["loc"]
				# 32768 * self.loc_scale + self.loc_offset
				a = -32768 * self.banis.loc_scale + self.banis.loc_offset
				b = 32768 * self.banis.loc_scale + self.banis.loc_offset
				self.locs[frame_i, bone_i] = np.interp(l, (0, 65535), (a, b))

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


class BanisFile(BanisRoot, IoFile):

	def __init__(self):
		super().__init__(BaniContext())
		# the output array
		self.bones_frames_eulers = []
		self.bones_frames_locs = []
		# input
		self.keys = []

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

	def save(self, filepath):
		self.num_frames, self.num_bones = self.data.shape
		with open(filepath, "wb") as stream:
			self.write_fields(stream, self)
			stream.write(self.data.tobytes())


if __name__ == "__main__":
	banis = BanisFile()
	banis.load("C:/Users/arnfi/Desktop/gila/gila_monster_idles.banisetc1b711e6 - just one anim.banis")
	# i = np.interp()
	x = np.linspace(-np.pi, np.pi, banis.num_frames)
	# sin_dat = (np.sin(x)+1)*32768
	sin_dat = np.sin(x)*25000 + 32768
	banis.data[:, 7]["loc"][:, 2] = sin_dat
	# sin2_dat = (np.sin(x)+1)*32768  # for ushort
	sin2_dat = np.sin(x)*2000-10834
	# print(sin2_dat)

	# it does not appear to be the normalized remainder of a quat
	# for bone in range(banis.num_bones):
	# 	print(bone)
	# 	for x, y, z in banis.data[:, bone]["euler"].astype(dtype=np.float32):
	# 		print(bone, math.sqrt(x*x+y*y+z*z))
	# banis.data[:, 7]["euler"][:, 0] = 0
	# banis.data[:, 7]["euler"][:, 2] = 32768
	# banis.data[:, 7]["euler"][:, 2] = sin2_dat
	# 0 = rotate about global X in blender
	# 1 = rotate about global Z in blender
	# 2 = rotate about global Y in blender
	head_keys = banis.data[:, 7]["euler"][:, 2]
	banis.save("C:/Users/arnfi/Desktop/gila/gila_monster_idles.banisetc1b711e6.banis")
	print(head_keys)
