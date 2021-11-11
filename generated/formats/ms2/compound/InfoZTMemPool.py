import numpy
from generated.array import Array
from generated.context import ContextReference


class InfoZTMemPool:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.unk_count = 0
		self.unks = numpy.zeros((self.unk_count, 2), dtype='ushort')
		self.set_defaults()

	def set_defaults(self):
		self.unk_count = 0
		self.unks = numpy.zeros((self.unk_count, 2), dtype='ushort')

	def read(self, stream):
		self.io_start = stream.tell()
		self.unk_count = stream.read_ushort()
		self.unks = stream.read_ushorts((self.unk_count, 2))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_ushort(self.unk_count)
		stream.write_ushorts(self.unks)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'InfoZTMemPool [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* unk_count = {self.unk_count.__repr__()}'
		s += f'\n	* unks = {self.unks.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
