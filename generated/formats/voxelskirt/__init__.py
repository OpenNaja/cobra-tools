import time
import numpy as np
import os
from generated.array import Array
from generated.formats.ovl.versions import *
from generated.formats.voxelskirt.compound.Data import Data
from generated.formats.voxelskirt.compound.Header import Header
# from generated.formats.ovl import *
from generated.formats.voxelskirt.compound.Material import Material
from generated.formats.voxelskirt.compound.PosInfo import PosInfo
from generated.formats.voxelskirt.compound.Size import Size
from generated.io import IoFile


class VoxelskirtFile(Header, IoFile):

	def __init__(self, ):
		super().__init__()

	def name_items(self, array):
		for item in array:
			item.name = self.names[item.id]

	def load(self, filepath):
		start_time = time.time()
		self.filepath = filepath
		self.basename = os.path.basename(self.filepath)
		print(f"Loading {self.basename}...")

		with self.reader(filepath) as stream:
			self.read(stream)
			self.eoh = stream.tell()
			# print(self)
			# print(self.eoh)

			stream.seek(self.eoh + self.info.name_buffer_offset)
			name_offsets = stream.read_uint64s((self.info.name_count,))
			self.names = []
			for offset in name_offsets:
				stream.seek(int(self.eoh + offset))
				self.names.append(stream.read_zstring())

			stream.seek(self.eoh + self.info.data_offset)
			self.datas = stream.read_types(Data, (), (self.info.data_count,))

			stream.seek(self.eoh + self.info.size_offset)
			self.sizes = stream.read_types(Size, (), (self.info.size_count,))

			stream.seek(self.eoh + self.info.position_offset)
			self.positions = stream.read_types(PosInfo, (), (self.info.position_count,))

			stream.seek(self.eoh + self.info.mat_offset)
			self.materials = stream.read_types(Material, (), (self.info.mat_count,))

			# assign names...
			for s in (self.datas, self.sizes, self.positions, self.materials):
				self.name_items(s)

			for data in self.datas:
				stream.seek(self.eoh + data.offset)
				if data.type == 0:
					data.im = stream.read_ubytes((self.info.x, self.info.y))
				elif data.type == 2:
					data.im = stream.read_floats((self.info.x, self.info.y))

			for pos in self.positions:
				stream.seek(self.eoh + pos.offset)
				# X, Z, Y, Euler Z rot
				pos.locs = stream.read_floats((pos.count, 4))

			for mat in self.materials:
				stream.seek(self.eoh + mat.offset)
				# 4 floats, could be a bounding sphere
				mat.locs = stream.read_floats((mat.count, 4))

			# read PC style height map and masks
			if self.info.height_array_size_pc:
				stream.seek(self.eoh)
				# same as the other games
				self.heightmap = stream.read_floats((self.info.x, self.info.y))
				# the same pixel of each layer is stored in 4 consecutive bytes
				self.weights = stream.read_ubytes((self.info.x, self.info.y, 4))

		print(f"Loaded {self.basename} in {time.time()-start_time:.2f} seconds!")

	def extract(self, ):
		"""Stores the embedded height map and masks as separate images, lossless."""
		start_time = time.time()
		import imageio
		bare_name = os.path.splitext(self.filepath)[0]
		if is_pc(self):
			imageio.imwrite(f"{bare_name}_height.tiff", self.heightmap)
			for i in range(4):
				imageio.imwrite(f"{bare_name}_mask{i}.png", self.weights[:, :, i], compress_level=2)
		else:
			for data in self.datas:
				if data.type == 0:
					imageio.imwrite(f"{bare_name}_{data.name}.png", data.im, compress_level=2)
				elif data.type == 2:
					imageio.imwrite(f"{bare_name}_{data.name}.tiff", data.im)
		print(f"Extracted maps from {self.basename} in {time.time()-start_time:.2f} seconds!")

	def save(self, filepath):
		print("Writing verts and tris to temporary buffer")


if __name__ == "__main__":
	import matplotlib
	import matplotlib.pyplot as plt
	m = VoxelskirtFile()
	files = ("C:/Users/arnfi/Desktop/deciduousskirt.voxelskirt",
			  "C:/Users/arnfi/Desktop/alpineskirt.voxelskirt",
			  "C:/Users/arnfi/Desktop/nublar.voxelskirt",
			   "C:/Users/arnfi/Desktop/savannahskirt.voxelskirt")
	# files = ("C:/Users/arnfi/Desktop/savannahskirt.voxelskirt",)
	# files = ("C:/Users/arnfi/Desktop/nublar.voxelskirt",)
	# files = ("C:/Users/arnfi/Desktop/alpineskirt.voxelskirt",)
	for f in files:
		# print(f)
		m.load(f)
		m.extract()
		#
		# fig, ax = plt.subplots()
		# # ax.imshow(m.rest)
		# # ax.imshow(m.weights.reshape((m.info.x, m.info.y, 4))[:,:,1])
		# # ax.plot(m.rest[:,:1], "o")
		# # ax.scatter(m.rest[:,:1], m.rest[:,2])
		# ax.scatter(m.positions[:,0], m.positions[:,2], m.positions[:,3]*20)
		# # x, z, y,
		#
		# # ax.set(xlabel='time (s)', ylabel='voltage (mV)',
		# # 	   title='About as simple as it gets, folks')
		# # ax.grid()
		#
		# fig.savefig("test.png")
		# plt.show()