from generated.formats.wsm.compound.WsmHeader import WsmHeader
from modules.formats.BaseFormat import MemStructLoader


class WsmLoader(MemStructLoader):
	extension = ".wsm"
	target_class = WsmHeader

	# def extract(self, out_dir, show_temp_files, progress_callback):
	# 	name = self.sized_str_entry.name
	# 	logging.info(f"Writing {name}")
	# 	ovl_header = self.pack_header(b"WSM ")
	#
	# 	out_path = out_dir(name)
	# 	with open(out_path, 'wb') as outfile:
	# 		outfile.write(ovl_header)
	# 		outfile.write(self.sized_str_entry.pointers[0].data)
	# 		for f in self.sized_str_entry.fragments:
	# 			outfile.write(f.pointers[1].data)
