import logging
from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_padding


class XmlconfigLoader(BaseFile):

	def create(self):
		data = self._get_data(self.file_entry.path)
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		f_0 = self.create_fragments(self.sized_str_entry, 1)[0]
		self.write_to_pool(f_0.pointers[1], 2, data)
		self.write_to_pool(self.sized_str_entry.pointers[0], 2, b'\x00' * 8)
		self.write_to_pool(f_0.pointers[0], 2, b'\x00' * 8)

	def collect(self):
		self.assign_ss_entry()
		self.assign_fixed_frags(1)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")

		if len(self.sized_str_entry.fragments) == 1:
			f_0 = self.sized_str_entry.fragments[0]
		else:
			raise AttributeError(f"Found wrong amount of frags [{len(self.sized_str_entry.fragments)}] for {name}")
		# write xml
		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			# 8 x b00
			# sized_str_entry.pointers[0].data
			# 8 x b00
			# outfile.write( f_0.pointers[0].data )
			# the actual xml data
			# often with extra junk at the end (probably z str)
			f_0.pointers[1].strip_zstring_padding()
			# strip the b00 zstr terminator byte
			outfile.write(f_0.pointers[1].data[:-1])
		return out_path,

	def load(self, file_path):
		data = self._get_data(file_path)
		self.sized_str_entry.fragments[0].pointers[1].update_data(data, update_copies=True)

	def _get_data(self, file_path):
		with open(file_path, 'rb') as stream:
			# add zero terminator
			data = stream.read() + b"\x00"
			return data + get_padding(len(data), 8)
