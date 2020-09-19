import typing


class BKHDSection:

# First Section of a soundback aux

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

	def read(self, stream):
		self.length = stream.read_uint()
		self.version = stream.read_uint()
		self.id_a = stream.read_uint()
		self.id_b = stream.read_uint()
		self.constant_a = stream.read_uint()
		self.constant_b = stream.read_uint()
		self.zeroes = [stream.read_byte() for _ in range(self.length - 20)]

	def write(self, stream):
		stream.write_uint(self.length)
		stream.write_uint(self.version)
		stream.write_uint(self.id_a)
		stream.write_uint(self.id_b)
		stream.write_uint(self.constant_a)
		stream.write_uint(self.constant_b)
		for item in self.zeroes: stream.write_byte(item)

	def __repr__(self):
		s = 'BKHDSection'
		s += '\nlength ' + self.length.__repr__()
		s += '\nversion ' + self.version.__repr__()
		s += '\nid_a ' + self.id_a.__repr__()
		s += '\nid_b ' + self.id_b.__repr__()
		s += '\nconstant_a ' + self.constant_a.__repr__()
		s += '\nconstant_b ' + self.constant_b.__repr__()
		s += '\nzeroes ' + self.zeroes.__repr__()
		s += '\n'
		return s