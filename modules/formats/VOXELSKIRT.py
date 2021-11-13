from generated.formats.voxelskirt import VoxelskirtFile
from modules.formats.BaseFormat import BaseFile


class VoxelskirtLoader(BaseFile):

	def create(self):
		pass

	def collect(self):
		self.assign_ss_entry()

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		print(f"\nWriting {name}")

		ovl_header = self.pack_header(b"VOXE")
		out_path = out_dir(name)
		buffers = self.sized_str_entry.data_entry.buffer_datas
		# write voxelskirt
		with open(out_path, 'wb') as outfile:
			# write the sized str and buffers
			# print(sized_str_entry.pointers[0].data)
			outfile.write(ovl_header)
			outfile.write(self.sized_str_entry.pointers[0].data)
			for buff in buffers:
				outfile.write(buff)
		return out_path,

	def load(self, file_path):
		vox = VoxelskirtFile()
		ss_bytes, buffer_bytes = vox.get_structs(file_path)
		self.sized_str_entry.data_entry.update_data((buffer_bytes,))
		self.sized_str_entry.pointers[0].update_data(ss_bytes, update_copies=True)

