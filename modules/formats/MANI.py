import logging
import struct
from modules.formats.BaseFormat import BaseFile


class ManisLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
				
	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")
		if not self.sized_str_entry.data_entry:
			raise AttributeError(f"No data entry for {name}")
		ss_data = self.sized_str_entry.pointers[0].data
		# print(len(ss_data), ss_data)
		buffers = self.sized_str_entry.data_entry.buffer_datas
		# print(len(buffers))
		ovl_header = self.pack_header(b"MANI")
		manis_header = struct.pack("<I", len(self.sized_str_entry.children))
	
		# sizedstr data + 3 buffers
		# sized str data gives general info
		# buffer 0 holds all mani infos - weirdly enough, its first 10 bytes come from the sized str data!
		# buffer 1 is list of hashes and zstrs for each bone name
		# buffer 2 has the actual keys
		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			outfile.write(ovl_header)
			outfile.write(manis_header)
			for mani in self.sized_str_entry.children:
				outfile.write(mani.name.encode() + b"\x00")
			outfile.write(ss_data)
			for buff in self.sized_str_entry.data_entry.buffers:
				outfile.write(buff.data)
	
		# for i, buff in enumerate(self.sized_str_entry.data_entry.buffers):
		# 	with open(out_path+str(i), 'wb') as outfile:
		# 		outfile.write(buff.data)
		# if "partials" in name:
		# data = ManisFormat.Data()
		# with open(out_path, "rb") as stream:
		# 	data.read(stream)
	
		return out_path,
