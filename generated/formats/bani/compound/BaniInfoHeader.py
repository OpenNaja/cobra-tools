import numpy
from generated.array import Array
from generated.context import ContextReference
from generated.formats.bani.compound.BaniFragmentData0 import BaniFragmentData0


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
		self.data = BaniFragmentData0(self.context, None, None)
		self.set_defaults()

	def set_defaults(self):
		self.magic = numpy.zeros((4), dtype='byte')
		self.banis_name = 0
		self.data = BaniFragmentData0(self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.magic = stream.read_bytes((4))
		self.banis_name = stream.read_zstring()
		self.data = stream.read_type(BaniFragmentData0, (self.context, None, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_bytes(self.magic)
		stream.write_zstring(self.banis_name)
		stream.write_type(self.data)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'BaniInfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* magic = {self.magic.__repr__()}'
		s += f'\n	* banis_name = {self.banis_name.__repr__()}'
		s += f'\n	* data = {self.data.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
