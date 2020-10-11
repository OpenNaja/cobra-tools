import typing


class Attrib:
	zero_0: int
	zero_1: int
	attrib: typing.List[int]
	zero_2: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zero_0 = 0
		self.zero_1 = 0
		self.attrib = []
		self.zero_2 = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.zero_0 = stream.read_uint()
		self.zero_1 = stream.read_uint()
		self.attrib = [stream.read_byte() for _ in range(4)]
		self.zero_2 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.zero_0)
		stream.write_uint(self.zero_1)
		for item in self.attrib: stream.write_byte(item)
		stream.write_uint(self.zero_2)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Attrib [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* zero_0 = ' + self.zero_0.__repr__()
		s += '\n	* zero_1 = ' + self.zero_1.__repr__()
		s += '\n	* attrib = ' + self.attrib.__repr__()
		s += '\n	* zero_2 = ' + self.zero_2.__repr__()
		s += '\n'
		return s
