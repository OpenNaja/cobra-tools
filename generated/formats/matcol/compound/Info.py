import typing


class Info:
	zero_0: int
	zero_1: int
	flags: typing.List[int]
	value: typing.List[float]
	zero_3: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zero_0 = 0
		self.zero_1 = 0
		self.flags = []
		self.value = []
		self.zero_3 = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.zero_0 = stream.read_uint()
		self.zero_1 = stream.read_uint()
		self.flags = [stream.read_byte() for _ in range(4)]
		self.value = [stream.read_float() for _ in range(4)]
		self.zero_3 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.zero_0)
		stream.write_uint(self.zero_1)
		for item in self.flags: stream.write_byte(item)
		for item in self.value: stream.write_float(item)
		stream.write_uint(self.zero_3)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Info [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* zero_0 = ' + self.zero_0.__repr__()
		s += '\n	* zero_1 = ' + self.zero_1.__repr__()
		s += '\n	* flags = ' + self.flags.__repr__()
		s += '\n	* value = ' + self.value.__repr__()
		s += '\n	* zero_3 = ' + self.zero_3.__repr__()
		s += '\n'
		return s
