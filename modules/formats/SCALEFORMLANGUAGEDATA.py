import struct

from generated.formats.ovl.versions import is_pc
from modules.formats.BaseFormat import BaseFile


def write_scaleformlanguagedata(ovl, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name
	print(f"\nWriting {name}")

	out_path = out_dir(name)
	with open(out_path, 'wb') as outfile:
		# write each of the fragments
		outfile.write(sized_str_entry.pointers[0].data)
		for frag in sized_str_entry.fragments:
			outfile.write(frag.pointers[0].data)
			outfile.write(frag.pointers[1].data)
	return out_path,


class ScaleformLoader(BaseFile):

	def collect(self, ovl, file_entry):
		self.assign_fixed_frags(ovl, file_entry, 1)
		f0_d0 = struct.unpack("<8I", self.sized_str_entry.fragments[0].pointers[0].data)
		if is_pc(self.ovl):
			# data is organized differently here
			pass
		else:
			font_declare_count = f0_d0[2]
			self.sized_str_entry.fragments += self.ovs.frags_from_pointer(self.sized_str_entry.fragments[0].pointers[1], font_declare_count * 2)
