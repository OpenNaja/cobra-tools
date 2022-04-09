import logging
import os

from generated.formats.bani import BaniFile
from modules.formats.BaseFormat import BaseFile
from modules.helpers import as_bytes


class BanisLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		all_bani_files = self.ovl.get_extract_files((), (".bani",), ignore=False)
		self.bani_files = []
		for bani in all_bani_files:
			b_ss = self.ovl.get_sized_str_entry(bani.name)
			ss_ptr = b_ss.pointers[0]
			# since we run this several times if we have several banis, only grab once
			if not b_ss.fragments:
				b_ss.fragments = self.ovs.frags_from_pointer(ss_ptr, 1)
			# check if the pointers match
			if b_ss.fragments[0].pointers[1] == self.sized_str_entry.pointers[0]:
				self.bani_files.append(bani)
				logging.debug(f"{bani.name} uses {self.file_entry.name}")
			else:
				logging.debug(f"{bani.name} uses a different banis file")

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
			outfile.write(self.sized_str_entry.pointers[0].data)
			outfile.write(buffers[0])

		for bani in self.bani_files:
			b_ss = self.ovl.get_sized_str_entry(bani.name)
			logging.info(f"Writing {bani.name}")
			f = b_ss.fragments[0]
			# write banis file
			out_path = out_dir(bani.name)
			with open(out_path, 'wb') as outfile:
				outfile.write(b"BANI")
				outfile.write(as_bytes(name))
				outfile.write(f.pointers[0].data)
			out_paths.append(out_path)
		return out_paths

	def load(self, file_path):
		ss, buffer_0 = self._get_data(file_path)
		self.sized_str_entry.data_entry.update_data((buffer_0,))
		self.sized_str_entry.pointers[0].update_data(ss, update_copies=True)
		banis_dir = os.path.dirname(file_path)
		for bani_file_name in os.listdir(banis_dir):
			if bani_file_name.endswith(".bani"):
				for bani_file in self.bani_files:
					if bani_file_name == bani_file.name:
						logging.debug(f"Found matching bani {bani_file_name}")
						fp = os.path.join(banis_dir, bani_file_name)
						f0 = self._get_bani_data(fp)
						b_ss = self.ovl.get_sized_str_entry(bani_file_name)
						b_ss.pointers[0].update_data(f0, update_copies=True)
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

