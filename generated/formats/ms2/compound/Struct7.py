import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.NasutoJointEntry import NasutoJointEntry
from generated.formats.ms2.compound.SmartPadding import SmartPadding
from generated.formats.ms2.compound.UACJoint import UACJoint


class Struct7:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# needed for ZTUAC
		self.weird_padding = SmartPadding(self.context, None, None)

		# repeat
		self.count_7 = 0

		# seen 0
		self.zero_0 = 0

		# usually 2 - only for recent versions of PZ
		self.count_2 = 0

		# only for recent versions of PZ
		self.zero_2 = 0

		# 36 bytes per entry
		self.unknown_list = Array(self.context)

		# 60 bytes per entry
		self.unknown_list = Array(self.context)

		# align list to multiples of 8
		self.padding = numpy.zeros(((8 - ((self.count_7 * 60) % 8)) % 8), dtype='ubyte')

		# in JWE2 velo69 bone info 1, could also be, 2 * 2 ubyte + 4 bytes padding
		# this catches elasmo
		self.array_2 = numpy.zeros((self.count_2), dtype='uint')
		self.set_defaults()

	def set_defaults(self):
		if self.context.version <= 13:
			self.weird_padding = SmartPadding(self.context, None, None)
		self.count_7 = 0
		self.zero_0 = 0
		if self.context.version >= 48:
			self.count_2 = 0
		if self.context.version >= 48:
			self.zero_2 = 0
		if self.context.version <= 13:
			self.unknown_list = Array(self.context)
		if self.context.version >= 32:
			self.unknown_list = Array(self.context)
		self.padding = numpy.zeros(((8 - ((self.count_7 * 60) % 8)) % 8), dtype='ubyte')
		if self.context.version >= 51:
			self.array_2 = numpy.zeros((self.count_2), dtype='uint')

	def read(self, stream):
		self.io_start = stream.tell()
		if self.context.version <= 13:
			self.weird_padding = stream.read_type(SmartPadding, (self.context, None, None))
		self.count_7 = stream.read_uint64()
		self.zero_0 = stream.read_uint64()
		if self.context.version >= 48:
			self.count_2 = stream.read_uint64()
			self.zero_2 = stream.read_uint64()
		if self.context.version <= 13:
			self.unknown_list.read(stream, UACJoint, self.count_7, None)
		if self.context.version >= 32:
			self.unknown_list.read(stream, NasutoJointEntry, self.count_7, None)
		self.padding = stream.read_ubytes(((8 - ((self.count_7 * 60) % 8)) % 8))
		if self.context.version >= 51:
			self.array_2 = stream.read_uints((self.count_2))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		if self.context.version <= 13:
			stream.write_type(self.weird_padding)
		stream.write_uint64(self.count_7)
		stream.write_uint64(self.zero_0)
		if self.context.version >= 48:
			stream.write_uint64(self.count_2)
			stream.write_uint64(self.zero_2)
		if self.context.version <= 13:
			self.unknown_list.write(stream, UACJoint, self.count_7, None)
		if self.context.version >= 32:
			self.unknown_list.write(stream, NasutoJointEntry, self.count_7, None)
		stream.write_ubytes(self.padding)
		if self.context.version >= 51:
			stream.write_uints(self.array_2)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Struct7 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* weird_padding = {self.weird_padding.__repr__()}'
		s += f'\n	* count_7 = {self.count_7.__repr__()}'
		s += f'\n	* zero_0 = {self.zero_0.__repr__()}'
		s += f'\n	* count_2 = {self.count_2.__repr__()}'
		s += f'\n	* zero_2 = {self.zero_2.__repr__()}'
		s += f'\n	* unknown_list = {self.unknown_list.__repr__()}'
		s += f'\n	* padding = {self.padding.__repr__()}'
		s += f'\n	* array_2 = {self.array_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
