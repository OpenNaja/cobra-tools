import typing
from generated.array import Array


class ManisSizedStrData:

	"""
	per attribute
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 96 in driver
		self.unknown_0 = 0

		# 272 in driver
		self.unknown_1 = 0

		# zeros in driver
		self.unknown_2 = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.unknown_0 = stream.read_ushort()
		self.unknown_1 = stream.read_ushort()
		self.unknown_2.read(stream, 'Uint', 5, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_ushort(self.unknown_0)
		stream.write_ushort(self.unknown_1)
		self.unknown_2.write(stream, 'Uint', 5, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'ManisSizedStrData [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* unknown_0 = ' + self.unknown_0.__repr__()
		s += '\n	* unknown_1 = ' + self.unknown_1.__repr__()
		s += '\n	* unknown_2 = ' + self.unknown_2.__repr__()
		s += '\n'
		return s
