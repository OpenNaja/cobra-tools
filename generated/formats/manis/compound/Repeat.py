import typing


class Repeat:
	zeros_0: typing.List[int]

	# to be read sequentially starting after this array
	byte_size: int
	zeros_1: typing.List[int]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zeros_0 = []
		self.byte_size = 0
		self.zeros_1 = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.zeros_0 = [stream.read_uint() for _ in range(15)]
		self.byte_size = stream.read_uint()
		self.zeros_1 = [stream.read_uint() for _ in range(4)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		for item in self.zeros_0: stream.write_uint(item)
		stream.write_uint(self.byte_size)
		for item in self.zeros_1: stream.write_uint(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Repeat [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* zeros_0 = ' + self.zeros_0.__repr__()
		s += '\n	* byte_size = ' + self.byte_size.__repr__()
		s += '\n	* zeros_1 = ' + self.zeros_1.__repr__()
		s += '\n'
		return s
