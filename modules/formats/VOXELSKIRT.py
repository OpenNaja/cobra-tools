import io
import logging
import os

import imageio.v3 as iio
import numpy as np

from generated.array import Array
from generated.formats.base.basic import Ubyte, Float, ZString
from generated.formats.ovl import is_pc
from generated.formats.voxelskirt.compounds.VoxelskirtRoot import VoxelskirtRoot
from modules.formats.BaseFormat import MemStructLoader
from modules.formats.shared import get_padding


class VoxelskirtLoader(MemStructLoader):
	extension = ".voxelskirt"
	target_class = VoxelskirtRoot

	def load_slot(self, data_slot, stream):
		stream.seek(data_slot._offset)
		data_slot.data = Array.from_stream(stream, self.header.context, 0, None, (data_slot._count, ), data_slot.template)

	def write_slot(self, data_slot, stream):
		data_slot._offset = stream.tell()
		data_slot._count = len(data_slot.data)
		Array.to_stream(data_slot.data, stream, self.header.context, 0, None, (data_slot._count, ), data_slot.data.dtype)

	def create(self):
		self.create_root_entry()
		self.header = self.target_class.from_xml_file(self.file_entry.path, self.ovl.context)
		stream = io.BytesIO()
		basepath = os.path.splitext(self.file_entry.path)[0]
		names_lut = {name.name: i for i, name in enumerate(self.header.names.data)}
		# write layers
		for layer in self.header.layers.data:
			layer._offset = stream.tell()
			# read layer from image file
			layer.im = iio.imread(self.get_file_path(layer, basepath))
			Array.to_stream(layer.im, stream, self.header.context, 0, None, (self.header.x, self.header.y), self.get_dtype(layer))
			layer._data_size = stream.tell() - layer._offset
		# write all named slots
		for data_slot in self.named_slots:
			# update name index before writing to stream
			for item in data_slot.data:
				item._id = names_lut[item.name]
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
		# clear the data slots before writing to pools
		for data_slot in self.named_slots:
			# todo - need to handle data so that it is available for export, but not written to header
			# probably by having behavior similar to the Pointer classes
			data_slot.data.clear()
		# need to update before writing ptrs
		self.header.write_ptrs(self, self.root_ptr, self.file_entry.pool_type)

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

		# get layers
		for layer in self.header.layers.data:
			stream.seek(layer._offset)
			layer.im = Array.from_stream(stream, self.header.context, 0, None, (self.header.x, self.header.y), self.get_dtype(layer))

		# get additional position slots
		for data_slot in (self.header.entity_groups, self.header.materials):
			for entry in data_slot.data:
				self.load_slot(entry.entity_instances, stream)

		# read PC style height map and masks
		if is_pc(self.ovl):
			stream.seek(0)
			# same as the other games
			self.heightmap = Array.from_stream(stream, self.header.context, 0, None, (self.header.x, self.header.y), Float)
			# the same pixel of each layer is stored in 4 consecutive bytes
			self.weights = Array.from_stream(stream, self.header.context, 0, None, (self.header.x, self.header.y, 4), Ubyte)

	def get_dtype(self, layer):
		if layer.dtype == 0:
			return Ubyte
		elif layer.dtype == 2:
			return Float
		else:
			raise NotImplementedError(f"Unsupported dtype {layer.dtype}")

	@property
	def named_slots(self):
		return self.header.layers, self.header.areas, self.header.entity_groups, self.header.materials

	def extract(self, out_dir):
		out_files = list(super().extract(out_dir))
		# out_files += self.dump_buffers(out_dir)
		basepath = out_dir(self.file_entry.basename)
		# print(self.header)
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

	def get_file_path(self, layer, basepath):
		if layer.dtype == 0:
			return f"{basepath}_{layer.name}.png"
		elif layer.dtype == 2:
			return f"{basepath}_{layer.name}.tiff"
		else:
			raise NotImplementedError(f"Unknown data type {layer.dtype}")
