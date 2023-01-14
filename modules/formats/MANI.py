import logging
import os
import struct

from generated.formats.manis.compounds.SizedStrData import SizedStrData
from generated.formats.manis import ManisFile
from modules.formats.BaseFormat import BaseFile
from modules.helpers import as_bytes


class ManiLoader(BaseFile):
	extension = ".mani"
	can_extract = False

	def create(self):
		self.create_root_entry()
		self.root_entry.struct_ptr.pool_index = -1


class ManisLoader(BaseFile):
	extension = ".manis"
				
	def extract(self, out_dir):
		name = self.root_entry.name
		logging.info(f"Writing {name}")
		if not self.data_entry:
			raise AttributeError(f"No data entry for {name}")
		# buffers = self.data_entry.buffer_datas
		# print(len(buffers))
		manis_header = struct.pack("<I", len(self.children))

		# sized str data gives general info
		# buffer 0 - all mani infos
		# buffer 1 - list of hashes and zstrs for each bone name
		# buffer 2 - actual keys
		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			outfile.write(struct.pack("<I", self.file_entry.mime.mime_version))
			outfile.write(manis_header)
			for mani in self.children:
				outfile.write(as_bytes(mani.file_entry.basename))
			outfile.write(self.root_ptr.data)
			for buff in self.data_entry.buffers:
				outfile.write(buff.data)
			# JWE2 can now have a secondary data entry holding a buffer 2 in an ovs
			for ovs_name, ext_data in self.data_entries.items():
				if ovs_name != "STATIC":
					logging.debug(f"Extracting from {ovs_name}")
					for buff in ext_data.buffers:
						outfile.write(buff.data)
	
		# for i, buff in enumerate(self.data_entry.buffers):
		# 	with open(out_path+str(i), 'wb') as outfile:
		# 		outfile.write(buff.data)
	
		return out_path,

	def create(self):
		manis_file, root_data, b0, b1, b2 = self._get_data(self.file_entry.path)
		ms2_dir = os.path.dirname(self.file_entry.path)

		self.create_root_entry()

		# create mani files
		for mani_name in manis_file.names:
			mani_path = os.path.join(ms2_dir, mani_name+".mani")
			mani_loader = self.ovl.create_file(mani_path)
			self.children.append(mani_loader)

		self.write_data_to_pool(self.root_entry.struct_ptr, self.file_entry.pool_type, root_data)
		self.create_data_entry((b0, b1, b2))

	def _get_data(self, file_path):
		"""Loads and returns the data for a manis"""
		manis_file = ManisFile()
		manis_file.load(file_path)
		return manis_file, as_bytes(manis_file.header), \
			as_bytes(manis_file.mani_infos), as_bytes(manis_file.name_buffer), \
			as_bytes(manis_file.keys_buffer)
