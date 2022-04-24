import logging

from generated.formats.wsm import WsmFile
from modules.formats.BaseFormat import BaseFile


class WsmLoader(BaseFile):
	extension = ".wsm"

	def collect(self):
		self.assign_ss_entry()
		self.assign_fixed_frags(2)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")
		ovl_header = self.pack_header(b"WSM ")

		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			outfile.write(ovl_header)
			outfile.write(self.sized_str_entry.pointers[0].data)
			for f in self.sized_str_entry.fragments:
				outfile.write(f.pointers[1].data)

		# dds_file = WsmFile()
		# dds_file.load(out_path)
		# print(dds_file)
		return out_path,
