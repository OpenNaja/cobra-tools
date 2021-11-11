from generated.array import Array
from generated.context import ContextReference
from generated.formats.ovl.compound.HeaderPointer import HeaderPointer


class Fragment:

	"""
	often huge amount of tiny files
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# points into header datas section
		self.pointers = Array(self.context)
		self.set_defaults()

	def set_defaults(self):
		self.pointers = Array(self.context)

	def read(self, stream):
		self.io_start = stream.tell()
		self.pointers.read(stream, HeaderPointer, 2, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.pointers.write(stream, HeaderPointer, 2, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Fragment [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* pointers = {self.pointers.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
