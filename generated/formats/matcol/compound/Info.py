import typing
from generated.array import Array


class Info:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zero_0 = 0
		self.zero_1 = 0
		self.flags = Array()
		self.value = Array()
		self.zero_3 = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.zero_0 = stream.read_uint()
		self.zero_1 = stream.read_uint()
		self.flags.read(stream, 'Byte', 4, None)
		self.value.read(stream, 'Float', 4, None)
		self.zero_3 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.zero_0)
		stream.write_uint(self.zero_1)
		self.flags.write(stream, 'Byte', 4, None)
		self.value.write(stream, 'Float', 4, None)
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
