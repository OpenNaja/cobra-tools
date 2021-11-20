from generated.array import Array
from generated.context import ContextReference
from generated.formats.ovl.compound.HeaderPointer import HeaderPointer


class DependencyEntry:

	"""
	Description of dependency; links it to an entry from this archive
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# Hash of this dependency, for lookup in hash dict. Can be either external or internal.
		self.file_hash = 0

		# offset for extension into string name table
		self.offset = 0

		# index into ovl file table, points to the file entry where this dependency is used
		self.file_index = 0

		# pointer into flattened list of all archives' pools
		self.pointers = Array((1), HeaderPointer, self.context, None, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.file_hash = 0
		self.offset = 0
		self.file_index = 0
		self.pointers = Array((1), HeaderPointer, self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.file_hash = stream.read_uint()
		self.offset = stream.read_uint()
		self.file_index = stream.read_uint()
		self.pointers.read(stream, HeaderPointer, 1, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.file_hash)
		stream.write_uint(self.offset)
		stream.write_uint(self.file_index)
		self.pointers.write(stream, HeaderPointer, 1, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'DependencyEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* file_hash = {self.file_hash.__repr__()}'
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* file_index = {self.file_index.__repr__()}'
		s += f'\n	* pointers = {self.pointers.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
