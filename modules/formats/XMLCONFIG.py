import logging
from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_padding


class XmlconfigLoader(BaseFile):
	extension = ".xmlconfig"

	def create(self):
		data = self._get_data(self.file_entry.path)
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		f_0 = self.create_fragments(self.sized_str_entry, 1)[0]
		self.write_to_pool(f_0.pointers[1], 2, data)
		self.write_to_pool(self.sized_str_entry.pointers[0], 2, b'\x00' * 16)
		self.ptr_relative(f_0.pointers[0], self.sized_str_entry.pointers[0], rel_offset=8)

	def collect(self):
		self.assign_ss_entry()
		self.assign_fixed_frags(1)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")
		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			outfile.write(self.p1_ztsr(self.sized_str_entry.fragments[0]))
		return out_path,

	def load(self, file_path):
		data = self._get_data(file_path)
		self.sized_str_entry.fragments[0].pointers[1].update_data(data, update_copies=True)

	@staticmethod
	def _get_data(file_path):
		with open(file_path, 'rb') as stream:
			# add zero terminator
			data = stream.read() + b"\x00"
			return data + get_padding(len(data), 8)
