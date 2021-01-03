import time
import numpy as np
import os
from generated.array import Array
from generated.formats.ovl.versions import *
from generated.formats.voxelskirt.compound.Data import Data
from generated.formats.voxelskirt.compound.Header import Header
# from generated.formats.ovl import *
from generated.formats.voxelskirt.compound.Size import Size
from generated.io import IoFile


class VoxelskirtFile(Header, IoFile):

	def __init__(self, ):
		super().__init__()

	def name_items(self, array):
		for item in array:
			item.name = self.names[item.id]

	def load(self, filepath):
		self.filepath = filepath
		start_time = time.time()
		# eof = super().load(filepath)

		# extra stuff
		self.bone_names = []
		self.bone_info = None
		with self.reader(filepath) as stream:
			self.read(stream)
			self.eoh = stream.tell()
			print(self)
			# self.heightmap = stream.read_floats((self.info.x, self.info.y))
			# print(f"Min Height: {np.min(self.heightmap)}, Max Height: {np.max(self.heightmap)}")
			# self.heightmap /= self.info.height
			# self.end_of_heightmap = stream.tell()
			# print(self.end_of_heightmap)
			# self.weights = stream.read_ubytes((self.info.x * self.info.y, 4))
			# print(self.weights)
			# self.end_of_weights = stream.tell()
			# print(self.end_of_weights)
			print(self.eoh)

			stream.seek(self.eoh + self.info.name_buffer_offset)
			name_offsets = stream.read_uint64s((self.info.name_count,))
			self.names = []
			for offset in name_offsets:
				# print(type(self.eoh), type(offset))
				stream.seek(int(self.eoh + offset))
				self.names.append(stream.read_zstring())
			stream.seek(self.eoh + self.info.data_offset)
			self.datas = stream.read_types(Data, (), (self.info.data_count,))

			stream.seek(self.eoh + self.info.size_offset)
			self.sizes = stream.read_types(Size, (), (self.info.size_count,))
			self.name_items(self.datas)
			self.name_items(self.sizes)
			print(self.names)
			print(self.datas)
			print(self.sizes)
			for data in self.datas:
				stream.seek(self.eoh + data.offset)
				if data.type == 0:
					data.im = stream.read_ubytes((self.info.x, self.info.y))
				elif data.type == 2:
					data.im = stream.read_floats((self.info.x, self.info.y))
				print(data.im)
			# # print(self.weights.shape)
			# # For non-PC maps, swap the axes so that the data layout is the same
			# if not is_pc(self):
			# 	# self.weights = np.swapaxes(self.weights, 0, 1)
			# 	# self.weights = np.moveaxis(self.weights, (0, 1), (1, 0))
			# 	self.weights = np.transpose(self.weights)
			# pos_size = self.info.io_size + self.info.io_start + self.info.data_offset - self.eoh
			# pos_count = pos_size // 16
			# print(pos_count)
			# self.positions = stream.read_floats((pos_count, 4))
			# print(self.positions)

	def extract(self, ):
		"""Stores the embedded height map and masks as separate images, lossless."""
		import imageio
		bare_name = os.path.splitext(self.filepath)[0]
		# num_layers = self.weights.shape[1]
		# layers = self.weights.reshape((self.info.x, self.info.y, num_layers))
		# imageio.imwrite(f"{bare_name}_height.tiff", self.heightmap)
		# for i in range(num_layers):
		# 	imageio.imwrite(f"{bare_name}_mask{i}.png", layers[:, :, i], compress_level=2)
		for data in self.datas:
			if data.type == 0:
				imageio.imwrite(f"{bare_name}_{data.name}.png", data.im, compress_level=2)
			elif data.type == 2:
				imageio.imwrite(f"{bare_name}_{data.name}.tiff", data.im)

	def save(self, filepath):
		print("Writing verts and tris to temporary buffer")


if __name__ == "__main__":
	import matplotlib
	import matplotlib.pyplot as plt
	m = VoxelskirtFile()
	# files = ("C:/Users/arnfi/Desktop/deciduousskirt.voxelskirt",
	# 		  "C:/Users/arnfi/Desktop/alpineskirt.voxelskirt",
	# 		  # "C:/Users/arnfi/Desktop/nublar.voxelskirt",
	# 		   "C:/Users/arnfi/Desktop/savannahskirt.voxelskirt")
	files = ("C:/Users/arnfi/Desktop/savannahskirt.voxelskirt",)
	# files = ("C:/Users/arnfi/Desktop/nublar.voxelskirt",)
	for f in files:
		print(f)
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