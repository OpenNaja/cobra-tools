import typing
from generated.array import Array


class Repeat:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zeros_0 = Array()

		# to be read sequentially starting after this array
		self.byte_size = 0
		self.zeros_1 = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.zeros_0.read(stream, 'Uint', 15, None)
		self.byte_size = stream.read_uint()
		self.zeros_1.read(stream, 'Uint', 4, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		self.zeros_0.write(stream, 'Uint', 15, None)
		stream.write_uint(self.byte_size)
		self.zeros_1.write(stream, 'Uint', 4, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Repeat [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* zeros_0 = ' + self.zeros_0.__repr__()
		s += '\n	* byte_size = ' + self.byte_size.__repr__()
		s += '\n	* zeros_1 = ' + self.zeros_1.__repr__()
		s += '\n'
		return s
