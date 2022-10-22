# START_GLOBALS
import logging
import io

from generated.formats.base.compounds.PadAlign import get_padding


# END_GLOBALS


class MemPool:

# START_CLASS

	def clear_data(self):
		self.new = False
		# lookup by offset
		self.offset_2_struct_entries = {}  # multiple (fragments') struct_ptrs can point to the same data
		self.offset_2_link_entry = {}  # link_ptrs are unique

	def get_first_entry(self):
		# usually 0, but be safe
		if self.offset_2_struct_entries:
			first_offset = sorted(self.offset_2_struct_entries.keys())[0]
			first_entries = self.offset_2_struct_entries[first_offset]
			if first_entries:
				return first_entries[0]

	def calc_struct_ptr_sizes(self):
		"""Assign an estimated size to every struct_ptr"""
		# sort them
		sorted_entries = sorted(self.offset_2_struct_entries.items())
		# add the end of the header data block
		sorted_entries.append((self.size, None))
		# get the size of each pointer
		for i, (offset, entries) in enumerate(sorted_entries[:-1]):
			# get the offset of the next pointer, substract this offset
			data_size = sorted_entries[i + 1][0] - offset
			for entry in entries:
				entry.struct_ptr.data_size = data_size

	def get_at(self, offset, size=-1):
		self.data.seek(offset)
		return self.data.read(size)

	def get_size(self):
		# seek to end of stream
		self.data.seek(0, 2)
		return self.data.tell()

	def pad(self, alignment=4):
		size = self.get_size()
		padding_bytes = get_padding(size, alignment)
		logging.debug(f"Padded pool of ({size} bytes) with {len(padding_bytes)}, alignment = {alignment}")
		self.data.write(padding_bytes)

	def move_empty_pointers_to_end(self):
		end_of_pool = self.get_size()
		# cast to tuple to avoid changing the dict during iteration
		for offset, entries in tuple(self.offset_2_struct_entries.items()):
			if offset != end_of_pool:
				# find any null pointer that is not at the end of the pool
				null_ptrs = [entry for entry in entries if entry.struct_ptr.data_size == 0]
				if null_ptrs:
					logging.debug(f"Moving {len(null_ptrs)} null pointers to end of pool at {end_of_pool}")
					# only keep valid pointers at offset
					self.offset_2_struct_entries[offset] = [entry for entry in entries if entry not in null_ptrs]
					# move the null pointers to their new offset
					if end_of_pool not in self.offset_2_struct_entries:
						self.offset_2_struct_entries[end_of_pool] = []
					self.offset_2_struct_entries[end_of_pool].extend(null_ptrs)
					# set data_offset of null_ptrs
					for entry in null_ptrs:
						entry.struct_ptr.data_offset = end_of_pool

