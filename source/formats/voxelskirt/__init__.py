import logging
import time
import numpy as np
import os
from generated.array import Array
from generated.formats.ovl.versions import *
from generated.formats.ovl_base import OvlContext
from generated.formats.ovl_base.basic import ConvStream
from generated.formats.voxelskirt.compound.Data import Data
from generated.formats.voxelskirt.compound.Header import Header
# from generated.formats.ovl.versions import *
from generated.formats.voxelskirt.basic import basic_map
from generated.formats.voxelskirt.compound.Material import Material
from generated.formats.voxelskirt.compound.PosInfo import PosInfo
from generated.formats.voxelskirt.compound.Size import Size
from generated.io import IoFile
from modules.formats.shared import get_padding_size, get_padding


class VoxelskirtFile(Header, IoFile):

	basic_map = basic_map

	def __init__(self, context):
		super().__init__(context)
		self.datas = Array(0, Data, self.context)
		self.sizes = Array(0, Size, self.context)
		self.positions = Array(0, PosInfo, self.context)
		self.materials = Array(0, Material, self.context)

	def name_items(self, array):
		for item in array:
			item.name = self.names[item.id]

	def load(self, filepath):
		start_time = time.time()
		self.filepath = filepath
		self.basename = os.path.basename(self.filepath)
		logging.info(f"Loading {self.basename}...")

		with self.reader(filepath) as stream:
			self.read(stream)
			self.eoh = stream.tell()
			# logging.info(self)
			# print(self.eoh)

			stream.seek(self.eoh + self.info.name_buffer_offset)
			name_offsets = stream.read_uint64s((self.info.name_count,))
			self.names = []
			for offset in name_offsets:
				stream.seek(int(self.eoh + offset))
				self.names.append(stream.read_zstring())

			stream.seek(self.eoh + self.info.data_offset)
			self.datas = Array.from_stream(stream, (self.info.data_count,), Data, self.context, 0, None)

			stream.seek(self.eoh + self.info.size_offset)
			self.sizes = Array.from_stream(stream, (self.info.size_count,), Size, self.context, 0, None)

			stream.seek(self.eoh + self.info.position_offset)
			self.positions = Array.from_stream(stream, (self.info.position_count,), PosInfo, self.context, 0, None)

			stream.seek(self.eoh + self.info.mat_offset)
			self.materials = Array.from_stream(stream, (self.info.mat_count,), Material, self.context, 0, None)

			# assign names...
			for s in (self.datas, self.sizes, self.positions, self.materials):
				self.name_items(s)
			# logging.info(self.sizes)

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

		logging.info(f"Loaded {self.basename} in {time.time()-start_time:.2f} seconds")

	def extract(self, ):
		"""Stores the embedded height map and masks as separate images, lossless."""
		start_time = time.time()
		image_paths = []
		import imageio
		bare_name = os.path.splitext(self.filepath)[0]
		if is_pc(self):
			p = f"{bare_name}_height.tiff"
			image_paths.append(p)
			imageio.imwrite(p, self.heightmap)
			for i in range(4):
				p = f"{bare_name}_mask{i}.png"
				image_paths.append(p)
				imageio.imwrite(p, self.weights[:, :, i], compress_level=2)
		else:
			for data in self.datas:
				if data.type == 0:
					p = f"{bare_name}_{data.name}.png"
					imageio.imwrite(p, data.im, compress_level=2)
				elif data.type == 2:
					p = f"{bare_name}_{data.name}.tiff"
					imageio.imwrite(p, data.im)
				else:
					logging.warning(f"Unknown data type {data.type}")
					continue
				image_paths.append(p)
		logging.info(f"Extracted {len(image_paths)} maps from {self.basename} in {time.time()-start_time:.2f} seconds")
		return image_paths

	def inject(self, filepaths):
		"""Replaces images"""
		start_time = time.time()
		import imageio
		for filepath in filepaths:
			im = imageio.imread(filepath)
			bare_name = os.path.splitext(filepath)[0]
			suffix = bare_name.rsplit("_", 1)[1]
			if is_pc(self):
				if suffix == "height":
					self.heightmap = im
				elif "mask" in suffix:
					try:
						i = int(suffix.replace("mask", ""))
					except:
						raise AttributeError(f"Broken suffix {suffix} for PC style.")
					self.weights[:, :, i] = im
				else:
					raise AttributeError(f"Unsupported suffix {suffix} for this file.")
			else:
				for data in self.datas:
					if data.name == suffix:
						break
				else:
					raise AttributeError(f"Could not find layer {suffix} in this file.")
				data.im = im
		print(f"Injected {len(filepaths)} layers into {self.basename} in {time.time()-start_time:.2f} seconds")

	def update_names(self, list_of_arrays):
		self.names = []
		for s in list_of_arrays:
			for item in s:
				if item.name not in self.names:
					self.names.append(item.name)
				item.id = self.names.index(item.name)

	def save(self, filepath):
		start_time = time.time()
		self.basename = os.path.basename(self.filepath)
		print(f"Saving {self.basename}...")

		# update data
		self.update_names((self.datas, self.sizes, self.positions, self.materials))
		if is_pc(self):
			self.info.height_array_size_pc = self.info.x * self.info.y * 4

		# write the buffer data to a temporary stream
		with ConvStream() as stream:
			# write the images
			if is_pc(self):
				stream.write_floats(self.heightmap)
				stream.write_ubytes(self.weights)
			else:
				# PC and JWE store the images attached to data infos
				for data in self.datas:
					data.offset = stream.tell()
					if data.type == 0:
						stream.write_ubytes(data.im)
					elif data.type == 2:
						stream.write_floats(data.im)

			self.info.data_offset = stream.tell()
			self.info.data_count = len(self.datas)
			Array.to_stream(stream, self.datas, (self.info.data_count,), Data, self.context, 0, None)

			self.info.size_offset = stream.tell()
			self.info.size_count = len(self.sizes)
			Array.to_stream(stream, self.sizes, (self.info.size_count,), Size, self.context, 0, None)

			# write object positions
			for pos in self.positions:
				pos.offset = stream.tell()
				stream.write_floats(pos.locs)
			self.info.position_offset = stream.tell()
			self.info.position_count = len(self.positions)
			Array.to_stream(stream, self.positions, (self.info.position_count,), PosInfo, self.context, 0, None)

			# write 'materials' / bbox / whatever
			for mat in self.materials:
				mat.offset = stream.tell()
				stream.write_floats(mat.locs)
			self.info.material_offset = stream.tell()
			self.info.material_count = len(self.materials)
			Array.to_stream(stream, self.materials, (self.info.material_count,), Material, self.context, 0, None)

			# write names
			name_addresses = []
			name_start = stream.tell()
			for name in self.names:
				name_addresses.append(stream.tell())
				stream.write_zstring(name)
			# pad name section
			stream.write(get_padding(stream.tell() - name_start, alignment=8))
			stream.write_uint64s(name_addresses)
			# get the actual result buffer
			buffer_bytes = stream.getvalue()

		# write the actual file
		with self.writer(filepath) as stream:
			self.write(stream)
			stream.write(buffer_bytes)
		print(f"Saved {self.basename} in {time.time()-start_time:.2f} seconds")

	def get_structs(self, filepath):
		with self.reader(filepath) as stream:
			self.read(stream)
			self.eoh = stream.tell()
			buffer_bytes = stream.read()
			stream.seek(self.info.io_start)
			sized_str_header = stream.read(self.info.io_size)
			return sized_str_header, buffer_bytes


if __name__ == "__main__":
	import matplotlib
	import matplotlib.pyplot as plt
	m = VoxelskirtFile()
	# files = ("C:/Users/arnfi/Desktop/deciduousskirt.voxelskirt",
	# 		  "C:/Users/arnfi/Desktop/alpineskirt.voxelskirt",
	# 		  "C:/Users/arnfi/Desktop/nublar.voxelskirt",
	# 		   "C:/Users/arnfi/Desktop/savannahskirt.voxelskirt")
	# files = ("C:/Users/arnfi/Desktop/savannahskirt.voxelskirt",)
	# files = ("C:/Users/arnfi/Desktop/nublar.voxelskirt",)
	# files = ("C:/Users/arnfi/Desktop/nublar2.voxelskirt",)
	files = ("C:/Users/arnfi/Desktop/nublar.voxelskirt", "C:/Users/arnfi/Desktop/nublar2.voxelskirt",)
	# files = ("C:/Users/arnfi/Desktop/alpineskirt.voxelskirt",)
	for f in files:
		# print(f)
		m.load(f)
		print(m)
		# m.extract()
		# m.inject(("C:/Users/arnfi/Desktop/nublar_playArea.png",))
		# m.positions[0].name = "TestObject"
		# m.save(f+"2")
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