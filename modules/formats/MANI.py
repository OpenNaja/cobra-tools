import logging
import os
import struct

from generated.formats.manis.compound.SizedStrData import SizedStrData
from generated.formats.manis import ManisFile
from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_versions
from modules.helpers import as_bytes


class ManisLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
				
	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")
		if not self.sized_str_entry.data_entry:
			raise AttributeError(f"No data entry for {name}")
		ss_ptr = self.sized_str_entry.pointers[0]
		# header = ss_ptr.load_as(SizedStrData)[0]
		# buffers = self.sized_str_entry.data_entry.buffer_datas
		# print(len(buffers))
		ovl_header = self.pack_header(b"MANI")
		manis_header = struct.pack("<I", len(self.sized_str_entry.children))

		# sized str data gives general info
		# buffer 0 - all mani infos
		# buffer 1 - list of hashes and zstrs for each bone name
		# buffer 2 - actual keys
		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			outfile.write(ovl_header)
			outfile.write(manis_header)
			for mani in self.sized_str_entry.children:
				outfile.write(as_bytes(mani.basename))
			outfile.write(ss_ptr.data)
			for buff in self.sized_str_entry.data_entry.buffers:
				outfile.write(buff.data)
	
		# for i, buff in enumerate(self.sized_str_entry.data_entry.buffers):
		# 	with open(out_path+str(i), 'wb') as outfile:
		# 		outfile.write(buff.data)
	
		return out_path,

	def create(self):
		manis_file, ss, b0, b1, b2 = self._get_data(self.file_entry.path)
		ms2_dir = os.path.dirname(self.file_entry.path)

		manis_entry = self.create_ss_entry(self.file_entry)
		manis_entry.children = []

		# create mani files
		for mani_name in manis_file.names:
			mani_path = os.path.join(ms2_dir, mani_name+".mani")
			mani_file_entry = self.get_file_entry(mani_path)

			mani_entry = self.create_ss_entry(mani_file_entry)
			mani_entry.pointers[0].pool_index = -1
			manis_entry.children.append(mani_entry)

		# todo - pool type
		self.write_to_pool(manis_entry.pointers[0], 2, ss)
		self.create_data_entry(manis_entry, (b0, b1, b2))

	def _get_data(self, file_path):
		"""Loads and returns the data for a manis"""
		versions = get_versions(self.ovl)
		manis_file = ManisFile()
		manis_file.load(file_path)
		return manis_file, as_bytes(manis_file.header, version_info=versions), \
			as_bytes(manis_file.mani_infos, version_info=versions), as_bytes(manis_file.name_buffer, version_info=versions), \
			as_bytes(manis_file.keys_buffer, version_info=versions)
