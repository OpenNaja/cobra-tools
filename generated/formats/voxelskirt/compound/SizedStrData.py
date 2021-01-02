import typing
from generated.array import Array


class SizedStrData:

	"""
	# 104 bytes
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zero = 0

		# total size of buffer data
		self.data_size = 0
		self.x = 0
		self.y = 0
		self.height = 0
		self.unk = Array()

		# x*y*4
		self.height_array_size = 0

		# slightly smaller than total size of buffer data
		self.data_offset_1 = 0
		self.a = 0
		self.unk_2 = Array()

		# slightly smaller than total size of buffer data
		self.data_offset_2 = 0
		self.b = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.zero = stream.read_uint64()
		self.data_size = stream.read_uint64()
		self.x = stream.read_uint64()
		self.y = stream.read_uint64()
		self.height = stream.read_float()
		self.unk.read(stream, 'Uint', 3, None)
		self.height_array_size = stream.read_uint64()
		self.data_offset_1 = stream.read_uint64()
		self.a = stream.read_uint64()
		self.unk_2.read(stream, 'Uint64', 2, None)
		self.data_offset_2 = stream.read_uint64()
		self.b = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64(self.zero)
		stream.write_uint64(self.data_size)
		stream.write_uint64(self.x)
		stream.write_uint64(self.y)
		stream.write_float(self.height)
		self.unk.write(stream, 'Uint', 3, None)
		stream.write_uint64(self.height_array_size)
		stream.write_uint64(self.data_offset_1)
		stream.write_uint64(self.a)
		self.unk_2.write(stream, 'Uint64', 2, None)
		stream.write_uint64(self.data_offset_2)
		stream.write_uint64(self.b)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'SizedStrData [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+'] ' + self.name
		s += '\n	* zero = ' + self.zero.__repr__()
		s += '\n	* data_size = ' + self.data_size.__repr__()
		s += '\n	* x = ' + self.x.__repr__()
		s += '\n	* y = ' + self.y.__repr__()
		s += '\n	* height = ' + self.height.__repr__()
		s += '\n	* unk = ' + self.unk.__repr__()
		s += '\n	* height_array_size = ' + self.height_array_size.__repr__()
		s += '\n	* data_offset_1 = ' + self.data_offset_1.__repr__()
		s += '\n	* a = ' + self.a.__repr__()
		s += '\n	* unk_2 = ' + self.unk_2.__repr__()
		s += '\n	* data_offset_2 = ' + self.data_offset_2.__repr__()
		s += '\n	* b = ' + self.b.__repr__()
		s += '\n'
		return s
