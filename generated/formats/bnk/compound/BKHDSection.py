import typing


class BKHDSection:

	"""
	First Section of a soundback aux
	"""

	# length of following data
	length: int
	version: int
	id_a: int
	id_b: int
	constant_a: int
	constant_b: int

	# filler zeroes
	zeroes: typing.List[int]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.length = 0
		self.version = 0
		self.id_a = 0
		self.id_b = 0
		self.constant_a = 0
		self.constant_b = 0
		self.zeroes = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.length = stream.read_uint()
		self.version = stream.read_uint()
		stream.version = self.version
		self.id_a = stream.read_uint()
		self.id_b = stream.read_uint()
		self.constant_a = stream.read_uint()
		self.constant_b = stream.read_uint()
		self.zeroes = [stream.read_byte() for _ in range(self.length - 20)]

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
		for item in self.zeroes: stream.write_byte(item)

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
