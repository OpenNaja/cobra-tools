import logging
import os

from generated.formats.bani import BaniFile
from generated.formats.bani.compound.BaniRoot import BaniRoot
from modules.formats.BaseFormat import BaseFile, MemStructLoader
from modules.helpers import as_bytes


class BaniLoader(MemStructLoader):
	extension = ".bani"
	target_class = BaniRoot

	def create(self):
		raise NotImplementedError

	def extract(self, out_dir, show_temp_files, progress_callback):
		logging.info(f"Writing {self.sized_str_entry.name}")

		# find banis name
		for ss in self.ovs.sized_str_entries:
			if self.header.banis.frag.struct_ptr == ss.struct_ptr:
				banis_name = ss.name
				break
		else:
			banis_name = "None"

		# write bani file
		out_path = out_dir(self.sized_str_entry.name)
		with open(out_path, 'wb') as outfile:
			outfile.write(b"BANI")
			outfile.write(as_bytes(banis_name))
			outfile.write(self.sized_str_entry.struct_ptr.data)

		return out_path,


class BanisLoader(BaseFile):
	extension = ".banis"

	def collect(self):
		self.assign_ss_entry()

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		if not self.sized_str_entry.data_entry:
			raise AttributeError(f"No data entry for {name}")
		buffers = self.sized_str_entry.data_entry.buffer_datas
		if len(buffers) != 1:
			raise AttributeError(f"Wrong amount of buffers for {name}")
		logging.info(f"Writing {name}")
		out_path = out_dir(name)
		out_paths = [out_path, ]
		with open(out_path, 'wb') as outfile:
			outfile.write(self.sized_str_entry.struct_ptr.data)
			outfile.write(buffers[0])

		return out_paths

	def load(self, file_path):
		ss, buffer_0 = self._get_data(file_path)
		self.sized_str_entry.data_entry.update_data((buffer_0,))
		self.sized_str_entry.struct_ptr.update_data(ss, update_copies=True)
		banis_dir = os.path.dirname(file_path)
		for bani_file_name in os.listdir(banis_dir):
			if bani_file_name.endswith(".bani"):
				for bani_file in self.bani_files:
					if bani_file_name == bani_file.name:
						logging.debug(f"Found matching bani {bani_file_name}")
						fp = os.path.join(banis_dir, bani_file_name)
						f0 = self._get_bani_data(fp)
						b_ss = self.ovl.get_sized_str_entry(bani_file_name)
						b_ss.struct_ptr.update_data(f0, update_copies=True)
						break

	def _get_data(self, file_path):
		with open(file_path, 'rb') as stream:
			header = stream.read(40)
			data = stream.read()
		return header, data

	def _get_bani_data(self, file_path):
		bani = BaniFile()
		bani.load(file_path)
		return as_bytes(bani.data)

