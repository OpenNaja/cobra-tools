import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.bani.compound.BaniFragmentData0 import BaniFragmentData0
from generated.formats.bani.compound.BaniFragmentData1 import BaniFragmentData1


class BaniInfoHeader:

	"""
	Custom header struct
	includes fragments but none of the 3 data buffers
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 'BANI'
		self.magic = numpy.zeros((4), dtype='byte')

		# name of the banis file buffer
		self.banis_name = 0
		self.data_0 = BaniFragmentData0(context, None, None)
		self.data_1 = BaniFragmentData1(context, None, None)

	def read(self, stream):

		self.io_start = stream.tell()
		self.magic = stream.read_bytes((4))
		self.banis_name = stream.read_string()
		self.data_0 = stream.read_type(BaniFragmentData0, (self.context, None, None))
		self.data_1 = stream.read_type(BaniFragmentData1, (self.context, None, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_bytes(self.magic)
		stream.write_string(self.banis_name)
		stream.write_type(self.data_0)
		stream.write_type(self.data_1)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'BaniInfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* magic = {self.magic.__repr__()}'
		s += f'\n	* banis_name = {self.banis_name.__repr__()}'
		s += f'\n	* data_0 = {self.data_0.__repr__()}'
		s += f'\n	* data_1 = {self.data_1.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
