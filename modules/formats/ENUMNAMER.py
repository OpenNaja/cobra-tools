import logging
import struct
from modules.formats.BaseFormat import BaseFile


class EnumnamerLoader(BaseFile):

	def create(self):
		ss = self.get_content(self.file_entry.path)
		pool_index, pool = self.get_pool(2)
		offset = pool.data.tell()
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		self.sized_str_entry.pointers[0].pool_index = pool_index
		self.sized_str_entry.pointers[0].data_offset = offset

		# replace \n with 0x00
		content = ss.decode('utf-8'). splitlines()
		count   = len(content)
		logging.debug(f"enumnamer {count} data {content}")

		# enum needs 8 bytes for the entry count, +8 bytes to point to the string list
		# then also needs 8 bytes per string + the stringz data 
		pool.data.write(struct.pack("<I8s", count, b''))  # room for 16 bytes

		# offset where first string starts
		doffset = pool.data.tell()

		# pack data now.. we are not doing rstrip to the lines.. worth considering to remove extra spaces
		pool.data.write("\00".join(content).encode('utf-8'))

		# new offset for list pointers
		poffset = pool.data.tell()

		# point the list frag to the end of the data now.
		new_frag0 = self.create_fragment()
		new_frag0.pointers[0].pool_index = pool_index
		new_frag0.pointers[0].data_offset = offset + 0x8
		new_frag0.pointers[1].pool_index = pool_index
		new_frag0.pointers[1].data_offset = poffset

		# for each line, add the frag ptr space and create the frag ptr
		for x in content:
			pool.data.write(struct.pack("<8s", b''))
			strfrag = self.create_fragment()
			strfrag.pointers[0].pool_index = pool_index
			strfrag.pointers[0].data_offset = poffset
			strfrag.pointers[1].pool_index = pool_index
			strfrag.pointers[1].data_offset = doffset

			poffset += 8
			doffset += len(x) + 1 # skip string lenght

		# done


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
		# enumnamer only has a list of strings
		out_path = out_dir(name)
		with open(out_path, 'w') as outfile:
			for f in self.sized_str_entry.vars:
				# convert from bytes to string, remove trailing 0x00 and add \n
				strval = f.pointers[1].data.decode('utf-8')
				if strval[-1] == '\x00':
					strval = strval[:-1]
				outfile.write(f"{strval}\n")
				#logging.debug(f"enumnamer {strval}")

		return out_path,
