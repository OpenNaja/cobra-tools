import logging
from struct import unpack

from modules.formats.BaseFormat import BaseFile


class AnimalresearchunlockssettingsLoader(BaseFile):

	def create(self, ovs, file_entry):
		pass

	def collect(self, ovl, file_entry):
		self.ovl = ovl
		self.ovs = ovl.static_archive.content
		self.get_sized_str_entry(file_entry)
		ss_pointer = self.sized_str_entry.pointers[0]
		_, count = unpack("<QQ", ss_pointer.data)
		logging.debug(ss_pointer.data)
		logging.debug(f"{file_entry.name} has {count} entries")
		self.assign_fixed_frags(ovl, file_entry, 1)
		frag = self.sized_str_entry.fragments[0]
		logging.debug(frag)
		p1 = frag.pointers[1]
		count_of_triples = count-1
		# plus 1 fragment of variable size - 40ish
		triples = self.ovs.frags_from_pointer(p1, (count_of_triples*3)+1)
		frags_pt_1 = self.ovs.get_frags_from_ptr_lut(p1, count_of_triples)
		for f in frags_pt_1:
			name = f.pointers[1].data
			logging.debug(f"new: {name}")

		# logging.debug(triples)
		b_set = set()
		self.sized_str_entry.fragments += triples
		for i in range(count_of_triples):
			triple = triples[i*3:i*3+3]
			a, b, c = triple
			name = a.pointers[1].data
			b_v0, b_v1 = unpack("<QQ", b.pointers[0].data)
			c_v0, c_v1 = unpack("<QQ", c.pointers[0].data)
			logging.debug(f"{name}, {b_v1}, {c_v1}")
			# another link - this is 1 frag, usually after ss frag, might be b_v1
			b_ptr = c.pointers[1]
			# this bugs out for some reason, so get count of individual ones
			# self.sized_str_entry.fragments += self.get_frags_from_ptr_lut(b_ptr, 1)
			b_set.add(b_ptr.data_offset)

			# more names
			c_ptr = c.pointers[1]
			names = self.ovs.frags_from_pointer(c_ptr, c_v1)
			for nf in names:
				name = nf.pointers[1].data
				# b_v0, b_v1 = unpack("<QQ", b.pointers[0].data)
				logging.debug(f"{name}, {nf.pointers[0].data}")
			self.sized_str_entry.fragments += names

		end_f = triples[-1]
		logging.debug(f"{end_f.pointers[1].data}, {end_f.pointers[0].data}")

		# names = self.ovs.get_frags_from_ptr_lut(p1, (count_of_triples*3)+1)
		self.sized_str_entry.fragments += triples

		logging.debug(f"{len(b_set)} following levels")
		rest = self.ovs.frags_from_pointer(frag.pointers[0], len(b_set))
		for nf in rest:
			name = nf.pointers[1].data
			assert nf.pointers[0].data == b'\x00' * 16
			logging.debug(f"following: {name}")
		self.sized_str_entry.fragments += rest
