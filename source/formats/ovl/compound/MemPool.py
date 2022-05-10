# START_GLOBALS
import logging
import io

from generated.formats.ovl_base.basic import ConvStream
from modules.formats.shared import get_padding


# END_GLOBALS


class MemPool:

# START_CLASS

	def clear_data(self):
		self.new = False
		# lookup by pointer 0
		self.offset_2_struct_entries = {}  # multiple (fragments') struct_ptrs can point to the same data
		self.offset_2_link_entry = {}  # link_ptrs are unique

	def get_first_entry(self):
		# usually 0, but be safe
		if self.offset_2_struct_entries:
			first_offset = sorted(self.offset_2_struct_entries.keys())[0]
			first_entries = self.offset_2_struct_entries[first_offset]
			if first_entries:
				return first_entries[0]

	def add_struct(self, entry):
		"""Adds an entry to the required tables of this pool"""
		offset = entry.struct_ptr.data_offset
		if offset not in self.offset_2_struct_entries:
			self.offset_2_struct_entries[offset] = []
		self.offset_2_struct_entries[offset].append(entry)

	def add_link(self, entry):
		"""Adds an entry to the required tables of this pool"""
		offset = entry.link_ptr.data_offset
		self.offset_2_link_entry[offset] = entry
		entry.link_ptr.data_size = 8

	def flush_pointers(self):
		"""Pre-writing step to convert all edits that were done on individual pointers back into the consolidated header
		data io block"""

		logging.debug(f"Flushing ptrs")
		# first, get all ptrs that have data to write
		sorted_structs_map = sorted(self.offset_2_struct_entries.items())

		stack = []
		last_offset = -1
		for i, (offset, structs) in enumerate(sorted_structs_map):
			for entry in structs:
				struct_ptr = entry.struct_ptr
				if struct_ptr._data is not None:
					if last_offset == offset:
						logging.warning(f"last offset is same as offset {offset}, skipping ptr for update")
						continue
					stack.append((struct_ptr, i, offset))
					last_offset = offset

		# check if rewriting is needed
		if not stack:
			return
		# create new data writer
		data = ConvStream()
		last_offset = 0
		logging.debug(f"Stack size = {len(stack)}")
		# now go sequentially over all ptrs in the stack
		for ptr, i, offset in stack:
			from_end_of_last_to_start_of_this = self.get_at(last_offset, size=offset-last_offset)
			# write old data before this chunk and new data
			data.write(from_end_of_last_to_start_of_this)
			logging.debug(f"Flushing stack member {i} at original offset {offset} to {data.tell()}")

			data.write(ptr._data)
			# update offset to end of the original pointer
			last_offset = offset + ptr.data_size
			# check delta
			# todo - padding
			ptr._padding_size = ptr.padding_size
			delta = (len(ptr._data) + ptr._padding_size) - (ptr.data_size + ptr.padding_size)
			# update new data size on pointer
			ptr.data_size = len(ptr._data)
			if delta:
				# logging.debug(f"data size of stack [len: {len(sorted_structs_map)}] member {i} has changed")
				# get all ptrs that point into this pool, but after this pointer
				if i < len(sorted_structs_map):
					for offset_later, entries in sorted_structs_map[i+1:]:
						# logging.debug(f"Moving {offset_later} to {offset_later+delta}")
						# update their data offsets
						# todo - this does not update dependencies, use self.offset_2_link_entry
						for e in entries:
							e.struct_ptr.data_offset += delta
							if hasattr(e, "link_ptr"):
								e.struct_ptr.data_offset += delta
			# remove from pointer map, so pool can be deleted if it's empty
			if not ptr._data:
				if offset in self.offset_2_struct_entries:
					logging.debug(f"Removed offset {offset} from pool")
					self.offset_2_struct_entries.pop(offset)
		# write the rest of the data
		data.write(self.get_at(last_offset))
		# clear pointer data and stack
		for ptr, i, offset in stack:
			ptr._data = None
		# overwrite internal data
		self.data = data

	def calc_pointer_sizes(self):
		"""Assign an estimated size to every pointer"""
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
