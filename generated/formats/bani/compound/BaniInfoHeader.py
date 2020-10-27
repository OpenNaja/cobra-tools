import typing
from generated.array import Array
from generated.formats.bani.compound.BaniFragmentData0 import BaniFragmentData0
from generated.formats.bani.compound.BaniFragmentData1 import BaniFragmentData1


class BaniInfoHeader:

	"""
	Custom header struct
	includes fragments but none of the 3 data buffers
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 'BANI'
		self.magic = Array()

		# name of the banis file buffer
		self.banis_name = 0
		self.data_0 = BaniFragmentData0()
		self.data_1 = BaniFragmentData1()

	def read(self, stream):

		self.io_start = stream.tell()
		self.magic.read(stream, 'Byte', 4, None)
		self.banis_name = stream.read_string()
		self.data_0 = stream.read_type(BaniFragmentData0)
		self.data_1 = stream.read_type(BaniFragmentData1)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		self.magic.write(stream, 'Byte', 4, None)
		stream.write_string(self.banis_name)
		stream.write_type(self.data_0)
		stream.write_type(self.data_1)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'BaniInfoHeader [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* magic = ' + self.magic.__repr__()
		s += '\n	* banis_name = ' + self.banis_name.__repr__()
		s += '\n	* data_0 = ' + self.data_0.__repr__()
		s += '\n	* data_1 = ' + self.data_1.__repr__()
		s += '\n'
		return s
