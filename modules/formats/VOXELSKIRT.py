import io
import logging

from generated.array import Array
from generated.formats.base.basic import Ubyte, Float, ZString
from generated.formats.voxelskirt import VoxelskirtFile
from generated.formats.voxelskirt.compounds.VoxelskirtRoot import VoxelskirtRoot
from modules.formats.BaseFormat import MemStructLoader


class VoxelskirtLoader(MemStructLoader):
	extension = ".voxelskirt"
	target_class = VoxelskirtRoot

	def create(self):
		self.create_root_entry()
		vox = VoxelskirtFile(self.ovl.context)
		root_data, buffer_bytes = vox.get_structs(self.file_entry.path)
		self.create_data_entry((buffer_bytes,))
		self.write_data_to_pool(self.root_entry.struct_ptr, 2, root_data)

	def extract(self, out_dir):
		name = self.root_entry.name
		logging.info(f"Writing {name}")
		print(self.header)
		stream = io.BytesIO(self.data_entry.buffer_datas[0])
		for data_slot in (self.header.datas, self.header.names):
			stream.seek(data_slot.offset)
			data_slot.data = Array.from_stream(stream, self.ovl.context, 0, None, (data_slot.count, ), data_slot.template)
		for data in self.header.datas.data:
			stream.seek(data.offset)
			if data.dtype == 0:
				data.im = Ubyte.read_array(stream, (self.header.x, self.header.y), self.ovl.context, 0, None)
			elif data.dtype == 2:
				data.im = Float.read_array(stream, (self.header.x, self.header.y), self.ovl.context, 0, None)
		for name in self.header.names.data:
			stream.seek(name.offset)
			name.name = ZString.from_stream(stream, self.ovl.context)
			print(name.name)
		# with open(out_path, 'wb') as outfile:
		# 	# write the sized str and buffers
		# 	# print(root_entry.struct_ptr.data)
		return self.dump_buffers(out_dir)
		# ovl_header = self.pack_header(b"VOXE")
		# out_path = out_dir(name)
		# out_paths = [out_path, ]
		# buffers = self.data_entry.buffer_datas
		# # write voxelskirt
		# with open(out_path, 'wb') as outfile:
		# 	# write the sized str and buffers
		# 	# print(root_entry.struct_ptr.data)
		# 	outfile.write(ovl_header)
		# 	outfile.write(self.root_entry.struct_ptr.data)
		# 	for buff in buffers:
		# 		outfile.write(buff)
		#
		# vox = VoxelskirtFile(self.ovl.context)
		# vox.load(out_path)
		# out_paths.extend(vox.extract())
		# return out_paths

