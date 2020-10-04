from generated.formats.bani.compound.BaniInfoHeader import BaniInfoHeader
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


class BaniFile(BaniInfoHeader, IoFile):

	def __init__(self):
		super().__init__()
		# the output array
		self.bones_frames_eulers = []
		self.bones_frames_locs = []
		# input
		self.keys = []

	def load(self, filepath):
		# store file name for later
		self.file = filepath
		self.dir, self.basename = os.path.split(filepath)
		self.file_no_ext = os.path.splitext(self.file)[0]

		with self.reader(filepath) as stream:
			self.read(stream)

		# read banis array according to bani header
		self.read_banis()

	def read_banis(self, ):
		# get banis file
		banis_path = os.path.join(self.dir, self.banis_name)

		# todo: check exists
		with open(banis_path, 'rb') as banis:
			# seek to the starting position
			banis.seek(self.data_0.read_start_frame * self.data_1.bytes_per_frame)

			dt = np.dtype([
				("euler", np.short, (3,)),
				("loc", np.ushort, (3,)),
			])

			ft = np.dtype([
				("euler", np.float32, (3,)),
				("loc", np.float32, (3,)),
			])
			# create function for doing interpolation of the desired ranges
			center = self.data_1.translation_center
			first = self.data_1.translation_first
			self.eulers = np.empty((self.data_0.num_frames, self.data_1.num_bones, 3), dtype=np.float32)
			self.locs = np.empty((self.data_0.num_frames, self.data_1.num_bones, 3), dtype=np.float32)
			# read the packed data
			data = np.fromfile(banis, dtype=dt, count=self.data_0.num_frames * self.data_1.num_bones)
			# convert to floats
			data = data.astype(ft)
			data = data.reshape((self.data_0.num_frames, self.data_1.num_bones))
			for frame_i in range(self.data_0.num_frames):
				for bone_i in range(self.data_1.num_bones):
					e = data[frame_i, bone_i]["euler"]
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

					l = data[frame_i, bone_i]["loc"]
					self.locs[frame_i, bone_i] = np.interp(l, (0, 65535), (first, center - first))

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
		with self.writer(filepath) as stream:
			# first header
			self.write(stream)
		# got to write the banis too


if __name__ == "__main__":
	bani = BaniFile()
	bani.load("C:/Users/arnfi/Desktop/parrot/parrot@flying.bani")
	# bani.save("C:/Users/arnfi/Desktop/parrot/parrot2.fgm")
	print(bani)
