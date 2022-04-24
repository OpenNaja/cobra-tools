
import logging
import io

from generated.formats.ovl_base.basic import ConvStream
from modules.formats.shared import get_padding


from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class MemPool:

	"""
	Description of one archive header entry
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# always 0
		self.zero_1 = 0

		# the number of bytes inside this mempool
		self.size = 0

		# byte offset from the start of the mempools region
		self.offset = 0

		# always 0
		self.zero_2 = 0

		# DJB hash of the first file that points into this mempool
		self.file_hash = 0

		# zero
		self.disney_zero = 0

		# unknown count (related to number of files or pointers)
		self.num_files = 0

		# unknown count (related to number of files or pointers)
		self.num_files = 0

		# JWE: DJB hash for extension, 0 for PZ
		self.ext_hash = 0

		# always 0
		self.zero_3 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if self.context.version >= 17:
			self.zero_1 = 0
		self.size = 0
		self.offset = 0
		if self.context.version <= 15:
			self.zero_2 = 0
		self.file_hash = 0
		if self.context.version <= 15:
			self.disney_zero = 0
		if self.context.version <= 15:
			self.num_files = 0
		if self.context.version >= 17:
			self.num_files = 0
		if self.context.version >= 19:
			self.ext_hash = 0
		if self.context.version >= 19:
			self.zero_3 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		if instance.context.version >= 17:
			instance.zero_1 = stream.read_uint64()
		instance.size = stream.read_uint()
		instance.offset = stream.read_uint()
		if instance.context.version <= 15:
			instance.zero_2 = stream.read_uint64()
		instance.file_hash = stream.read_uint()
		if instance.context.version <= 15:
			instance.disney_zero = stream.read_ushort()
			instance.num_files = stream.read_ushort()
		if instance.context.version >= 17:
			instance.num_files = stream.read_uint()
		if instance.context.version >= 19:
			instance.ext_hash = stream.read_uint()
			instance.zero_3 = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		if instance.context.version >= 17:
			stream.write_uint64(instance.zero_1)
		stream.write_uint(instance.size)
		stream.write_uint(instance.offset)
		if instance.context.version <= 15:
			stream.write_uint64(instance.zero_2)
		stream.write_uint(instance.file_hash)
		if instance.context.version <= 15:
			stream.write_ushort(instance.disney_zero)
			stream.write_ushort(instance.num_files)
		if instance.context.version >= 17:
			stream.write_uint(instance.num_files)
		if instance.context.version >= 19:
			stream.write_uint(instance.ext_hash)
			stream.write_uint(instance.zero_3)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'MemPool [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* zero_1 = {fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* size = {fmt_member(self.size, indent+1)}'
		s += f'\n	* offset = {fmt_member(self.offset, indent+1)}'
		s += f'\n	* zero_2 = {fmt_member(self.zero_2, indent+1)}'
		s += f'\n	* file_hash = {fmt_member(self.file_hash, indent+1)}'
		s += f'\n	* disney_zero = {fmt_member(self.disney_zero, indent+1)}'
		s += f'\n	* num_files = {fmt_member(self.num_files, indent+1)}'
		s += f'\n	* ext_hash = {fmt_member(self.ext_hash, indent+1)}'
		s += f'\n	* zero_3 = {fmt_member(self.zero_3, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s

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
		sorted_items_filtered = [(offset, pointers) for offset, pointers in sorted_items if any(p.is_struct_ptr for p in pointers)]
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

