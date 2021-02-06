import typing
from generated.array import Array


class Ms2BufferInfoZT:

	"""
	Fragment data describing a MS2 buffer giving the size of the whole vertex and tri buffer.
	266 bytes
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.unks = Array()
		self.unks_1 = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.unks = stream.read_ushorts((7))
		self.unks_1 = stream.read_ushorts((126))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_ushorts(self.unks)
		stream.write_ushorts(self.unks_1)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Ms2BufferInfoZT [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* unks = {self.unks.__repr__()}'
		s += f'\n	* unks_1 = {self.unks_1.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
