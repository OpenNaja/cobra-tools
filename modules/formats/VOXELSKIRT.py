import io
import logging
import imageio.v3 as iio

from generated.array import Array
from generated.formats.base.basic import Ubyte, Float, ZString
from generated.formats.ovl import is_pc
from generated.formats.voxelskirt.compounds.EntityInstance import EntityInstance
from generated.formats.voxelskirt.compounds.VoxelskirtRoot import VoxelskirtRoot
from modules.formats.BaseFormat import MemStructLoader


class VoxelskirtLoader(MemStructLoader):
	extension = ".voxelskirt"
	target_class = VoxelskirtRoot

	def create(self):
		self.create_root_entry()
		self.header = self.target_class.from_xml_file(self.file_entry.path, self.ovl.context)
		stream = io.BytesIO()
		# print(self.header)
		for data_slot in self.named_slots:
			data_slot.offset = stream.tell()
			Array.to_stream(stream, data_slot.data, (len(data_slot.data), ), data_slot.data.dtype, self.ovl.context, 0, None)
			# need to handle this so that it is available for export, but not written to header
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
			stream.seek(data_slot.offset)
			data_slot.data = Array.from_stream(stream, self.ovl.context, 0, None, (data_slot.count, ), data_slot.template)

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
				slot = entry.entity_instances
				stream.seek(slot.offset)
				slot.data = Array.from_stream(stream, self.ovl.context, 0, None, (slot.count, ), slot.template)

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

