import logging
import struct
from modules.formats.BaseFormat import BaseFile
from modules.helpers import as_bytes


class EnumnamerLoader(BaseFile):

	def create(self):
		ss = self.get_content(self.file_entry.path)
		content = ss.decode('utf-8').splitlines()
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		root_f = self.create_fragments(self.sized_str_entry, 1)[0]
		self.sized_str_entry.vars = self.create_fragments(self.sized_str_entry, len(content))

		# write the options
		for option, frag in zip(content, self.sized_str_entry.vars):
			self.write_to_pool(frag.pointers[1], 2, as_bytes(option))
		# apparently no padding
		# self.sized_str_entry.vars[-1].pointers[1].pool.pad(alignment=4)
		for frag in self.sized_str_entry.vars:
			self.write_to_pool(frag.pointers[0], 4, b"\x00" * 8)
		self.write_to_pool(self.sized_str_entry.pointers[0], 4, struct.pack("<Q", len(content)))
		self.write_to_pool(root_f.pointers[0], 4, b"\x00" * 8)
		# point to start of options array
		self.ptr_relative(root_f.pointers[1], self.sized_str_entry.vars[0].pointers[0])

	def collect(self):
		self.assign_ss_entry()
		# Sized string initpos = position of first fragment
		self.assign_fixed_frags(1)
		count, _ = struct.unpack("<2I", self.sized_str_entry.pointers[0].data)
		self.sized_str_entry.vars = self.ovs.frags_from_pointer(self.sized_str_entry.fragments[0].pointers[1], count)
		# pointers[1].data is the name
		for var in self.sized_str_entry.vars:
			var.pointers[1].strip_zstring_padding()
		# The last fragment has padding that may be junk data to pad the size of the name block to multiples of 64
		self.sized_str_entry.fragments.extend(self.sized_str_entry.vars)

	def load(self, file_path):
		pass

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.debug(f"Writing {name}")
		# only has a list of strings
		out_path = out_dir(name)
		with open(out_path, 'w') as outfile:
			for f in self.sized_str_entry.vars:
				outfile.write(f"{self.get_zstr(f.pointers[1].data)}\n")
		return out_path,
