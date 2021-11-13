import logging

from modules.formats.BaseFormat import BaseFile
from modules.helpers import write_sized_str


class BanisLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		self.bani_files = self.ovl.get_extract_files((), (".bani",), [], ignore=False)
		for bani in self.bani_files:
			b_ss = self.ovl.get_sized_str_entry(bani.name)
			ss_pointer = b_ss.pointers[0]
			b_ss.fragments = self.ovs.frags_from_pointer(ss_pointer, 1)

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
			outfile.write(buffers[0])

		for bani in self.bani_files:
			b_ss = self.ovl.get_sized_str_entry(bani.name)
			logging.info(f"Writing {bani.name}")
			if len(b_ss.fragments) != 1:
				raise AttributeError(f"{bani.name} must have 1 fragment")
			f = b_ss.fragments[0]
			# write banis file
			out_path = out_dir(bani.name)
			with open(out_path, 'wb') as outfile:
				outfile.write(b"BANI")
				write_sized_str(outfile, name)
				outfile.write(f.pointers[0].data)
				outfile.write(f.pointers[1].data)
			out_paths.append(out_path)
		return out_paths


