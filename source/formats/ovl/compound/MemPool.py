# START_GLOBALS
import logging
import io

from generated.io import BinaryStream
from modules.formats.shared import get_padding


# END_GLOBALS


class MemPool:

# START_CLASS

	def flush_pointers(self, ignore_unaccounted_bytes=False):
		"""Pre-writing step to convert all edits that were done on individual pointers back into the consolidated header
		data io block"""

		logging.debug(f"Flushing ptrs")
		# first, get all ptrs that have data to write
		sorted_ptrs_map = sorted(self.pointer_map.items())

		stack = []
		last_offset = -1
		for i, (offset, pointers) in enumerate(sorted_ptrs_map):
			for ptr in pointers:
				if ptr._data is not None:
					if last_offset == offset:
						logging.warning(f"last offset is same as offset {offset}, skipping ptr for update")
						continue
					stack.append((ptr, i, offset))
					last_offset = offset

		# check if rewriting is needed
		if not stack:
			return
		# create new data writer
		data = BinaryStream()
		last_offset = 0
		logging.debug(f"Stack size = {len(stack)}")
		# now go sequentially over all ptrs in the stack
		for ptr, i, offset in stack:
			from_end_of_last_to_start_of_this = self.get_at(last_offset, size=offset-last_offset)
			# write old data before this chunk and new data
			data.write(from_end_of_last_to_start_of_this)
			logging.debug(f"Flushing stack member {i} at original offset {offset} to {data.tell()}")

			data.write(ptr._data)
			# update offset to end of the original ptr
			last_offset = offset + ptr.data_size
			# check delta
			# todo - padding
			ptr._padding_size = ptr.padding_size
			delta = (len(ptr._data) + ptr._padding_size) - (ptr.data_size + ptr.padding_size)
			# update new data size on ptr
			ptr.data_size = len(ptr._data)
			if delta:
				# logging.debug(f"data size of stack [len: {len(sorted_ptrs_map)}] member {i} has changed")
				# get all ptrs that point into this pool, but after this ptr
				if i < len(sorted_ptrs_map):
					for offset_later, pointers in sorted_ptrs_map[i+1:]:
						# logging.debug(f"Moving {offset_later} to {offset_later+delta}")
						# update their data offsets
						for p in pointers:
							p.data_offset += delta
			# remove from ptr map, so pool can be deleted if it's empty
			if not ptr._data:
				if offset in self.pointer_map:
					logging.debug(f"Removed offset {offset} from pool")
					self.pointer_map.pop(offset)
		# write the rest of the data
		data.write(self.get_at(last_offset))
		# clear ptr data and stack
		for ptr, i, offset in stack:
			ptr._data = None
		# overwrite internal data
		self.data = data

	def calc_pointer_sizes(self):
		"""Assign an estimated size to every pointer"""
		# calculate pointer data sizes
		# make them unique and sort them
		sorted_items = sorted(self.pointer_map.items())
		# pick all ptrs except frag ptr0
		sorted_items_filtered = [(offset, pointers) for offset, pointers in sorted_items if any(p.is_ref_ptr for p in pointers)]
		# logging.info(f"len(sorted_items) {len(sorted_items)}, len(sorted_items_filtered) {len(sorted_items_filtered)}")
		# add the end of the header data block
		sorted_items_filtered.append((self.size, None))
		# get the size of each pointer
		for i, (offset, pointers) in enumerate(sorted_items_filtered[:-1]):
			# get the offset of the next pointer, substract this offset
			data_size = sorted_items_filtered[i + 1][0] - offset
			for pointer in pointers:
				pointer.data_size = data_size

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
