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


class VoxelskirtLoader(MemStructLoader):
	extension = ".voxelskirt"
	target_class = VoxelskirtRoot

	def load_slot(self, data_slot, stream):
		stream.seek(data_slot.offset)
		data_slot.data = Array.from_stream(stream, self.header.context, 0, None, (data_slot.count, ), data_slot.template)

	def create(self):
		self.create_root_entry()
		self.header = self.target_class.from_xml_file(self.file_entry.path, self.ovl.context)
		stream = io.BytesIO()
		basepath = os.path.splitext(self.file_entry.path)[0]
		names_lut = {name.name: i for i, name in enumerate(self.header.names.data)}
		# print(self.header)
		# write layers
		for layer in self.header.layers.data:
			layer.offset = stream.tell()
			# read layer from image file
			layer.im = iio.imread(self.get_file_path(layer, basepath))
			Array.to_stream(layer.im, stream, self.header.context, 0, None, (self.header.x, self.header.y), self.get_dtype(layer))
			layer.dsize = stream.tell() - layer.offset
		for data_slot in self.named_slots:
			data_slot.offset = stream.tell()
			Array.to_stream(data_slot.data, stream, self.header.context, 0, None, (len(data_slot.data), ), data_slot.data.dtype)
			# update name index
			for item in data_slot.data:
				item._id = names_lut[item.name]
		# write names
		for name in self.header.names.data:
			name.offset = stream.tell()
			ZString.to_stream(name.name, stream, self.header.context)

		# take the finished buffer and create a data entry
		buffer_bytes = stream.getvalue()
		self.create_data_entry((buffer_bytes,))
		self.header.data_size = len(buffer_bytes)
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
			stream.seek(name.offset)
			name.name = ZString.from_stream(stream, self.header.context)

		# assign names
		for data_slot in self.named_slots:
			for item in data_slot.data:
				item.name = self.header.names.data[item._id].name

		# get layers
		for layer in self.header.layers.data:
			stream.seek(layer.offset)
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

	# def inject(self, filepaths):
	# 	"""Replaces images"""
	# 	start_time = time.time()
	# 	import imageio.v3 as iio
	# 	for filepath in filepaths:
	# 		im = iio.imread(filepath)
	# 		bare_name = os.path.splitext(filepath)[0]
	# 		suffix = bare_name.rsplit("_", 1)[1]
	# 		if is_pc(self):
	# 			if suffix == "height":
	# 				self.heightmap = im
	# 			elif "mask" in suffix:
	# 				try:
	# 					i = int(suffix.replace("mask", ""))
	# 				except:
	# 					raise AttributeError(f"Broken suffix {suffix} for PC style.")
	# 				self.weights[:, :, i] = im
	# 			else:
	# 				raise AttributeError(f"Unsupported suffix {suffix} for this file.")
	# 		else:
	# 			for data in self.datas:
	# 				if data.name == suffix:
	# 					break
	# 			else:
	# 				raise AttributeError(f"Could not find layer {suffix} in this file.")
	# 			data.im = im
	# 	print(f"Injected {len(filepaths)} layers into {self.basename} in {time.time()-start_time:.2f} seconds")
	#
	# def update_names(self, list_of_arrays):
	# 	self.names = []
	# 	for s in list_of_arrays:
	# 		for item in s:
	# 			if item.name not in self.names:
	# 				self.names.append(item.name)
	# 			item.id = self.names.index(item.name)
	#
	# def save(self, filepath):
	# 	start_time = time.time()
	# 	self.basename = os.path.basename(self.filepath)
	# 	print(f"Saving {self.basename}...")
	#
	# 	# update data
	# 	self.update_names((self.datas, self.sizes, self.positions, self.materials))
	# 	if is_pc(self):
	# 		self.info.height_array_size_pc = self.info.x * self.info.y * 4
	#
	# 	# write the buffer data to a temporary stream
	# 	with BytesIO() as stream:
	# 		# write the images
	# 		if is_pc(self):
	# 			stream.write_floats(self.heightmap)
	# 			stream.write_ubytes(self.weights)
	# 		else:
	# 			# PC and JWE store the images attached to data infos
	# 			for data in self.datas:
	# 				data.offset = stream.tell()
	# 				if data.type == 0:
	# 					stream.write_ubytes(data.im)
	# 				elif data.type == 2:
	# 					stream.write_floats(data.im)
	#
	# 		self.info.data_offset = stream.tell()
	# 		self.info.data_count = len(self.datas)
	# 		Array.to_stream(stream, self.datas, Data)
	#
	# 		self.info.size_offset = stream.tell()
	# 		self.info.size_count = len(self.sizes)
	# 		Array.to_stream(stream, self.sizes, Size)
	#
	# 		# write object positions
	# 		for pos in self.positions:
	# 			pos.offset = stream.tell()
	# 			stream.write_floats(pos.locs)
	# 		self.info.position_offset = stream.tell()
	# 		self.info.position_count = len(self.positions)
	# 		Array.to_stream(stream, self.positions, PosInfo)
	#
	# 		# write 'materials' / bbox / whatever
	# 		for mat in self.materials:
	# 			mat.offset = stream.tell()
	# 			stream.write_floats(mat.locs)
	# 		self.info.material_offset = stream.tell()
	# 		self.info.material_count = len(self.materials)
	# 		Array.to_stream(stream, self.materials, Material)
	#
	# 		# write names
	# 		name_addresses = []
	# 		name_start = stream.tell()
	# 		for name in self.names:
	# 			name_addresses.append(stream.tell())
	# 			stream.write_zstring(name)
	# 		# pad name section
	# 		stream.write(get_padding(stream.tell() - name_start, alignment=8))
	# 		stream.write_uint64s(name_addresses)
	# 		# get the actual result buffer
	# 		buffer_bytes = stream.getvalue()
	#
	# 	# write the actual file
	# 	with open(filepath, "wb") as stream:
	# 		self.write_fields(stream, self)
	# 		stream.write(buffer_bytes)
	# 	print(f"Saved {self.basename} in {time.time()-start_time:.2f} seconds")
