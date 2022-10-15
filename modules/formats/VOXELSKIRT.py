import io
import logging
import imageio.v3 as iio

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
		data_slot.data = Array.from_stream(stream, self.ovl.context, 0, None, (data_slot.count, ), data_slot.template)

	def create(self):
		self.create_root_entry()
		self.header = self.target_class.from_xml_file(self.file_entry.path, self.ovl.context)
		stream = io.BytesIO()
		# print(self.header)
		for data_slot in self.named_slots:
			data_slot.offset = stream.tell()
			Array.to_stream(data_slot.data, stream, self.header.context, (len(data_slot.data), ), data_slot.data.dtype, self.ovl.context, 0, None)
			# todo - need to handle data so that it is available for export, but not written to header
			# probably by having behavior similar to the Pointer classes
			data_slot.data.clear()
		# ...
		buffer_bytes = stream.getvalue()
		self.create_data_entry((buffer_bytes,))
		self.header.data_size = len(buffer_bytes)
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
			name.name = ZString.from_stream(stream, self.ovl.context)

		# assign names
		for data_slot in self.named_slots:
			for item in data_slot.data:
				item.name = self.header.names.data[item.id].name
			# print(data_slot.data)

		# get layers
		for layer in self.header.layers.data:
			stream.seek(layer.offset)
			if layer.dtype == 0:
				layer.im = Ubyte.read_array(stream, (self.header.x, self.header.y), self.ovl.context, 0, None)
			elif layer.dtype == 2:
				layer.im = Float.read_array(stream, (self.header.x, self.header.y), self.ovl.context, 0, None)

		# get additional position slots
		for data_slot in (self.header.entity_groups, self.header.materials):
			for entry in data_slot.data:
				self.load_slot(entry.entity_instances, stream)

		# read PC style height map and masks
		if is_pc(self.ovl):
			stream.seek(0)
			# same as the other games
			self.heightmap = Float.read_array(stream, (self.header.x, self.header.y), self.ovl.context, 0, None)
			# the same pixel of each layer is stored in 4 consecutive bytes
			self.weights = Ubyte.read_array(stream, (self.header.x, self.header.y, 4), self.ovl.context, 0, None)

	@property
	def named_slots(self):
		return self.header.layers, self.header.areas, self.header.entity_groups, self.header.materials

	def extract(self, out_dir):
		out_files = list(super().extract(out_dir))
		# out_files += self.dump_buffers(out_dir)
		basename = out_dir(self.file_entry.basename)
		# print(self.header)
		if is_pc(self.ovl):
			p = f"{basename}_height.tiff"
			out_files.append(p)
			iio.imwrite(p, self.heightmap)
			for i in range(4):
				p = f"{basename}_mask{i}.png"
				out_files.append(p)
				iio.imwrite(p, self.weights[:, :, i], compress_level=2)
		else:
			for layer in self.header.layers.data:
				if layer.dtype == 0:
					p = f"{basename}_{layer.name}.png"
					iio.imwrite(p, layer.im, compress_level=2)
				elif layer.dtype == 2:
					p = f"{basename}_{layer.name}.tiff"
					iio.imwrite(p, layer.im)
				else:
					logging.warning(f"Unknown data type {layer.type}")
					continue
				out_files.append(p)
		return out_files

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
