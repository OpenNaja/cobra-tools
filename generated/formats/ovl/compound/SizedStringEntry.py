from generated.array import Array
from generated.context import ContextReference
from generated.formats.ovl.compound.HeaderPointer import HeaderPointer


class SizedStringEntry:

	"""
	Main file entry in the ovs
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# id (index or djb) of the file
		self.file_hash = 0

		# djb of extension
		self.ext_hash = 0

		# one pointer OR -1 pointer for assets
		self.pointers = Array((1), HeaderPointer, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.file_hash = 0
		if self.context.version >= 19:
			self.ext_hash = 0
		self.pointers = Array((1), HeaderPointer, self.context, 0, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.file_hash = stream.read_uint()
		if self.context.version >= 19:
			self.ext_hash = stream.read_uint()
		self.pointers.read(stream, HeaderPointer, 1, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.file_hash)
		if self.context.version >= 19:
			stream.write_uint(self.ext_hash)
		self.pointers.write(stream, HeaderPointer, 1, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'SizedStringEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* file_hash = {self.file_hash.__repr__()}'
		s += f'\n	* ext_hash = {self.ext_hash.__repr__()}'
		s += f'\n	* pointers = {self.pointers.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
