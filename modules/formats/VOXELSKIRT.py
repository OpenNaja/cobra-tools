import logging

from generated.formats.voxelskirt import VoxelskirtFile
from modules.formats.BaseFormat import BaseFile


class VoxelskirtLoader(BaseFile):
	extension = ".voxelskirt"

	def create(self):
		self.create_root_entry()
		vox = VoxelskirtFile(self.ovl.context)
		root_entry_bytes, buffer_bytes = vox.get_structs(self.file_entry.path)
		self.create_data_entry((buffer_bytes,))
		self.write_data_to_pool(self.root_entry.struct_ptr, 2, root_entry_bytes)

	def extract(self, out_dir):
		name = self.root_entry.name
		logging.info(f"Writing {name}")

		ovl_header = self.pack_header(b"VOXE")
		out_path = out_dir(name)
		out_paths = [out_path, ]
		buffers = self.data_entry.buffer_datas
		# write voxelskirt
		with open(out_path, 'wb') as outfile:
			# write the sized str and buffers
			# print(root_entry.struct_ptr.data)
			outfile.write(ovl_header)
			outfile.write(self.root_entry.struct_ptr.data)
			for buff in buffers:
				outfile.write(buff)

		vox = VoxelskirtFile(self.ovl.context)
		vox.load(out_path)
		out_paths.extend(vox.extract())
		return out_paths

