import io
import logging
import os

import imageio.v3 as iio
import numpy as np

from generated.array import Array
from generated.formats.base.basic import Ubyte, Float, ZString
from generated.formats.ovl import is_pc
from modules.formats.BaseFormat import MemStructLoader
from modules.formats.shared import get_padding
from generated.formats.voxelskirt.structs.VoxelskirtRoot import VoxelskirtRoot
from generated.formats.voxelskirt.structs.VoxelTerrainMaterialLayerSpecRoot import VoxelTerrainMaterialLayerSpecRoot
from generated.formats.voxelskirt.structs.VoxelTerrainMaterialAssetPackagesRoot import VoxelTerrainMaterialAssetPackagesRoot


logging.getLogger('PIL').setLevel(logging.WARNING)

def read_layer_image(uri):
	if uri.endswith(".tiff"):
		# not sure if we need to do any resampling here, assume proper float32 data
		return iio.imread(uri)
	else:
		# make sure the image editors didn't mess up,
		# using pngs with palettes requires a conversion
		return iio.imread(uri, mode="RGBA")[:, :, 0]


class VoxelskirtLoader(MemStructLoader):
	extension = ".voxelskirt"
	target_class = VoxelskirtRoot

	def create(self, file_path):
		self.header = self.target_class.from_xml_file(file_path, self.ovl.context)
		stream = io.BytesIO()
		basepath = os.path.splitext(file_path)[0]
		names_lut = {name.name: i for i, name in enumerate(self.header.names.data)}
		# write layers
		if is_pc(self.ovl):
			# load images first
			self.heightmap = read_layer_image(f"{basepath}_height.tiff")
			self.weights = np.empty((self.header.x, self.header.y, 4), np.uint8)
			for i in range(4):
				self.weights[:, :, i] = read_layer_image(f"{basepath}_mask{i}.png")
			self.header._height_offset = stream.tell()
			# height is same format as the other games
			Array.to_stream(self.heightmap, stream, self.header.context, 0, None, (self.header.x, self.header.y), Float)
			# weights store the same pixel of each layer in 4 consecutive bytes
			self.header._weights_offset = stream.tell()
			Array.to_stream(self.weights, stream, self.header.context, 0, None, (self.header.x, self.header.y, 4), Ubyte)
		else:
			for layer in self.header.layers.data:
				layer._offset = stream.tell()
				# read layer from image file
				layer.im = read_layer_image(self.get_file_path(layer, basepath))
				Array.to_stream(layer.im, stream, self.header.context, 0, None, (self.header.x, self.header.y), self.get_dtype(layer))
				layer._data_size = stream.tell() - layer._offset
		# write all named slots
		for data_slot in self.named_slots:
			# update name index before writing to stream
			if data_slot.data is not None:
				for item in data_slot.data:
					item._id = names_lut[item.name]
					if hasattr(item, "entity_instances"):
						self.write_slot(item.entity_instances, stream)
				self.write_slot(data_slot, stream)
		# write names
		for name in self.header.names.data:
			name._offset = stream.tell()
			ZString.to_stream(name.name, stream, self.header.context)
		# pad to at least 8 (maybe 16?)
		stream.write(get_padding(stream.tell(), alignment=8))
		# write name references
		self.write_slot(self.header.names, stream)

		# take the finished buffer and create a data entry
		buffer_bytes = stream.getvalue()
		self.create_data_entry((buffer_bytes,))
		self.header._data_size = len(buffer_bytes)
		# need to update before writing ptrs
		self.write_memory_data()

	def collect(self):
		super().collect()
		stream = io.BytesIO(self.data_entry.buffer_datas[0])

		# read the arrays
		for data_slot in (*self.named_slots, self.header.names):
			self.load_slot(data_slot, stream)

		# get names
		for name in self.header.names.data:
			stream.seek(name._offset)
			name.name = ZString.from_stream(stream, self.header.context)

		# assign names
		for data_slot in self.named_slots:
			for item in data_slot.data:
				item.name = self.header.names.data[item._id].name
				# get additional position slots
				if hasattr(item, "entity_instances"):
					self.load_slot(item.entity_instances, stream)

		# read PC style height map and masks
		if is_pc(self.ovl):
			# same format as the other games
			stream.seek(self.header._height_offset)
			self.heightmap = Array.from_stream(stream, self.header.context, 0, None, (self.header.x, self.header.y), Float)
			# the same pixel of each layer is stored in 4 consecutive bytes
			stream.seek(self.header._weights_offset)
			self.weights = Array.from_stream(stream, self.header.context, 0, None, (self.header.x, self.header.y, 4), Ubyte)
		else:
			# get layers
			for layer in self.header.layers.data:
				stream.seek(layer._offset)
				layer.im = Array.from_stream(stream, self.header.context, 0, None, (self.header.x, self.header.y), self.get_dtype(layer))

	def extract(self, out_dir):
		out_files = list(super().extract(out_dir))
		basepath = out_dir(self.basename)
		if is_pc(self.ovl):
			p = f"{basepath}_height.tiff"
			out_files.append(p)
			iio.imwrite(p, self.heightmap)
			for i in range(4):
				p = f"{basepath}_mask{i}.png"
				out_files.append(p)
				iio.imwrite(p, self.weights[:, :, i], compress_level=2)
		else:
			for layer in self.header.layers.data:
				p = self.get_file_path(layer, basepath)
				iio.imwrite(p, layer.im)  # , compress_level=2
				out_files.append(p)
		return out_files

	def get_dtype(self, layer):
		if layer.dtype == 0:
			return Ubyte
		elif layer.dtype == 2:
			return Float
		else:
			raise NotImplementedError(f"Unsupported dtype {layer.dtype}")

	def get_file_path(self, layer, basepath):
		if layer.dtype == 0:
			return f"{basepath}_{layer.name}.png"
		elif layer.dtype == 2:
			return f"{basepath}_{layer.name}.tiff"
		else:
			raise NotImplementedError(f"Unknown data type {layer.dtype}")

	@property
	def named_slots(self):
		return self.header.layers, self.header.areas, self.header.entity_groups, self.header.materials

	def load_slot(self, data_slot, stream):
		stream.seek(data_slot._offset)
		data_slot.data = Array.from_stream(stream, self.header.context, 0, None, (data_slot._count, ), data_slot.template)

	def write_slot(self, data_slot, stream):
		data_slot._count = len(data_slot.data)
		if data_slot._count:
			data_slot._offset = stream.tell()
			Array.to_stream(data_slot.data, stream, self.header.context, 0, None, (data_slot._count, ), data_slot.data.dtype)
		else:
			data_slot._offset = 0


class VoxelTerrainMaterialLayerSpecLoader(MemStructLoader):
	extension = ".vtmls"
	target_class = VoxelTerrainMaterialLayerSpecRoot

class VoxelTerrainMaterialAssetPackagesRootLoader(MemStructLoader):
	extension = ".vtmap"
	target_class = VoxelTerrainMaterialAssetPackagesRoot
