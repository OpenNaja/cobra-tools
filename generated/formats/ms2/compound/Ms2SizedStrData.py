import numpy
import typing
from generated.array import Array
from generated.context import ContextReference


class Ms2SizedStrData:

	"""
	Read at the entry point of the sized str entry for the ms2. Seems to be the 'root header' of the ms2.
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 32 if PC, 47 if JWE, 48 if PZ
		self.ms_2_version = 0

		# 1 if yes, 0 if no
		self.vertex_buffer_count = 0

		# 3 in stairwell
		self.mdl_2_count = 0

		# count of names in ms2 buffer0
		self.name_count = 0

		# usually 0, rarely 1
		self.unk_count = 0

		# seems to be zeros
		self.unknown_1 = numpy.zeros((3), dtype='uint')

	def read(self, stream):

		self.io_start = stream.tell()
		self.ms_2_version = stream.read_uint()
		self.context.ms_2_version = self.ms_2_version
		self.vertex_buffer_count = stream.read_ushort()
		self.mdl_2_count = stream.read_ushort()
		self.name_count = stream.read_ushort()
		self.unk_count = stream.read_ushort()
		self.unknown_1 = stream.read_uints((3))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.ms_2_version)
		self.context.ms_2_version = self.ms_2_version
		stream.write_ushort(self.vertex_buffer_count)
		stream.write_ushort(self.mdl_2_count)
		stream.write_ushort(self.name_count)
		stream.write_ushort(self.unk_count)
		stream.write_uints(self.unknown_1)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Ms2SizedStrData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* ms_2_version = {self.ms_2_version.__repr__()}'
		s += f'\n	* vertex_buffer_count = {self.vertex_buffer_count.__repr__()}'
		s += f'\n	* mdl_2_count = {self.mdl_2_count.__repr__()}'
		s += f'\n	* name_count = {self.name_count.__repr__()}'
		s += f'\n	* unk_count = {self.unk_count.__repr__()}'
		s += f'\n	* unknown_1 = {self.unknown_1.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
