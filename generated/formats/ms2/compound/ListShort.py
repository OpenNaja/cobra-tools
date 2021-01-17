import typing
from generated.array import Array


class ListShort:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.floats = Array()
		self.a = 0
		self.b = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.floats = stream.read_floats((8))
		self.a = stream.read_ushort()
		self.b = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_floats(self.floats)
		stream.write_ushort(self.a)
		stream.write_ushort(self.b)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ListShort [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* floats = {self.floats.__repr__()}'
		s += f'\n	* a = {self.a.__repr__()}'
		s += f'\n	* b = {self.b.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
