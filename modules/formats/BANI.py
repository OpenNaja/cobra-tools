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
		logging.info(f"Writing {self.root_entry.name}")

		# find banis name
		for root_entry in self.ovs.root_entries:
			if self.header.banis.frag.struct_ptr == root_entry.struct_ptr:
				banis_name = root_entry.name
				break
		else:
			banis_name = "None"

		# write bani file
		out_path = out_dir(self.root_entry.name)
		with open(out_path, 'wb') as outfile:
			outfile.write(b"BANI")
			outfile.write(as_bytes(banis_name))
			outfile.write(self.root_entry.struct_ptr.data)

		return out_path,


class BanisLoader(BaseFile):
	extension = ".banis"

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.root_entry.name
		if not self.data_entry:
			raise AttributeError(f"No data entry for {name}")
		buffers = self.data_entry.buffer_datas
		if len(buffers) != 1:
			raise AttributeError(f"Wrong amount of buffers for {name}")
		logging.info(f"Writing {name}")
		out_path = out_dir(name)
		out_paths = [out_path, ]
		with open(out_path, 'wb') as outfile:
			outfile.write(self.root_entry.struct_ptr.data)
			outfile.write(buffers[0])

		return out_paths

	def load(self, file_path):
		# todo - fixme
		root_entry, buffer_0 = self._get_data(file_path)
		self.data_entry.update_data((buffer_0,))
		self.write_data_to_pool(self.root_entry.struct_ptr, 2, root_entry)
		banis_dir = os.path.dirname(file_path)
		for bani_file_name in os.listdir(banis_dir):
			if bani_file_name.endswith(".bani"):
				for bani_file in self.bani_files:
					if bani_file_name == bani_file.name:
						logging.debug(f"Found matching bani {bani_file_name}")
						fp = os.path.join(banis_dir, bani_file_name)
						f0 = self._get_bani_data(fp)
						b_ss, archive = self.ovl.get_root_entry(bani_file_name)
						self.write_data_to_pool(b_ss.struct_ptr, 2, f0)
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

