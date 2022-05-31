import logging
import os
import struct

from generated.formats.manis.compound.SizedStrData import SizedStrData
from generated.formats.manis import ManisFile
from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_versions
from modules.helpers import as_bytes


class ManiLoader(BaseFile):

	def create(self):
		self.create_root_entry()
		self.root_entry.struct_ptr.pool_index = -1


class ManisLoader(BaseFile):
	extension = ".manis"
				
	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.root_entry.name
		logging.info(f"Writing {name}")
		if not self.data_entry:
			raise AttributeError(f"No data entry for {name}")
		# buffers = self.data_entry.buffer_datas
		# print(len(buffers))
		ovl_header = self.pack_header(b"MANI")
		manis_header = struct.pack("<I", len(self.children))

		# sized str data gives general info
		# buffer 0 - all mani infos
		# buffer 1 - list of hashes and zstrs for each bone name
		# buffer 2 - actual keys
		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			outfile.write(ovl_header)
			outfile.write(manis_header)
			for mani in self.children:
				outfile.write(as_bytes(mani.file_entry.basename))
			outfile.write(self.root_ptr.data)
			for buff in self.data_entry.buffers:
				outfile.write(buff.data)
	
		# for i, buff in enumerate(self.data_entry.buffers):
		# 	with open(out_path+str(i), 'wb') as outfile:
		# 		outfile.write(buff.data)
	
		return out_path,

	def create(self):
		manis_file, root_entry, b0, b1, b2 = self._get_data(self.file_entry.path)
		ms2_dir = os.path.dirname(self.file_entry.path)

		self.create_root_entry()

		# create mani files
		for mani_name in manis_file.names:
			mani_path = os.path.join(ms2_dir, mani_name+".mani")
			mani_file_entry = self.get_file_entry(mani_path)
			mani_file_entry.loader.create()
			self.children.append(mani_file_entry.loader)

		# todo - pool type
		self.write_data_to_pool(self.root_entry.struct_ptr, 2, root_entry)
		self.create_data_entry((b0, b1, b2))

	def _get_data(self, file_path):
		"""Loads and returns the data for a manis"""
		versions = get_versions(self.ovl)
		manis_file = ManisFile()
		manis_file.load(file_path)
		return manis_file, as_bytes(manis_file.header, version_info=versions), \
			as_bytes(manis_file.mani_infos, version_info=versions), as_bytes(manis_file.name_buffer, version_info=versions), \
			as_bytes(manis_file.keys_buffer, version_info=versions)
