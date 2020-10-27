import typing
from generated.array import Array


class BKHDSection:

	"""
	First Section of a soundback aux
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# length of following data
		self.length = 0
		self.version = 0
		self.id_a = 0
		self.id_b = 0
		self.constant_a = 0
		self.constant_b = 0

		# filler zeroes
		self.zeroes = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.length = stream.read_uint()
		self.version = stream.read_uint()
		stream.version = self.version
		self.id_a = stream.read_uint()
		self.id_b = stream.read_uint()
		self.constant_a = stream.read_uint()
		self.constant_b = stream.read_uint()
		self.zeroes.read(stream, 'Byte', self.length - 20, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.length)
		stream.write_uint(self.version)
		stream.version = self.version
		stream.write_uint(self.id_a)
		stream.write_uint(self.id_b)
		stream.write_uint(self.constant_a)
		stream.write_uint(self.constant_b)
		self.zeroes.write(stream, 'Byte', self.length - 20, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'BKHDSection [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* length = ' + self.length.__repr__()
		s += '\n	* version = ' + self.version.__repr__()
		s += '\n	* id_a = ' + self.id_a.__repr__()
		s += '\n	* id_b = ' + self.id_b.__repr__()
		s += '\n	* constant_a = ' + self.constant_a.__repr__()
		s += '\n	* constant_b = ' + self.constant_b.__repr__()
		s += '\n	* zeroes = ' + self.zeroes.__repr__()
		s += '\n'
		return s
