# START_GLOBALS
import logging
import io
from modules.formats.shared import get_padding


# END_GLOBALS


class MemPool:

# START_CLASS

	def flush_pointers(self, ignore_unaccounted_bytes=False):
		"""Pre-writing step to convert all edits that were done on individual pointers back into the consolidated header
		data io block"""
		if self.update_from_ptrs:
			# maintain sorting order
			# grab the first pointer for each address
			# it is assumed that subsequent pointers to that address share the same data
			sorted_first_pointers = [pointers[0] for offset, pointers in sorted(self.pointer_map.items())]
			if sorted_first_pointers:
				# only known from indominus
				first_offset = sorted_first_pointers[0].data_offset
				if first_offset != 0 and not ignore_unaccounted_bytes:
					logging.debug(f"Found {first_offset} unaccounted bytes at start of header data {i}")
					unaccounted_bytes = self.data.getvalue()[:first_offset]
				else:
					unaccounted_bytes = b""

				# clear io objects
				self.data = io.BytesIO()
				self.data.write(unaccounted_bytes)
				# write updated strings
				for pointer in sorted_first_pointers:
					pointer.write_data(update_copies=True)
			else:
				# todo - shouldn't we delete the pool in that case?
				logging.debug(f"No pointers into pool {self.offset} - keeping its stock data!")

	def calc_pointer_sizes(self):
		"""Assign an estimated size to every pointer"""
		# calculate pointer data sizes
		# make them unique and sort them
		sorted_items = sorted(self.pointer_map.items())
		# add the end of the header data block
		sorted_items.append((self.size, None))
		# get the size of each pointer
		for i, (offset, pointers) in enumerate(sorted_items[:-1]):
			# get the offset of the next pointer, substract this offset
			data_size = sorted_items[i + 1][0] - offset
			# also calculate address of pointer
			address = self.address + offset
			for pointer in pointers:
				pointer.data_size = data_size
				pointer.address = address
				pointer.copies = pointers
				pointer.read_data()

	def pad(self, alignment=4):
		if self.update_from_ptrs:
			self.data.write(get_padding(self.data.tell(), alignment))
