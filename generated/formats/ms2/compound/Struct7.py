import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.NasutoJointEntry import NasutoJointEntry
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

		# guess for ZTUAC rhino
		self.zeros_start = numpy.zeros((6), dtype='ubyte')

		# repeat
		self.count_7 = 0

		# seen 0
		self.zero = 0

		# only for recent versions of PZ
		self.zeros_pz = numpy.zeros((2), dtype='uint64')

		# 36 bytes per entry
		self.unknown_list = Array(self.context)

		# 60 bytes per entry
		self.unknown_list = Array(self.context)

		# align list to multiples of 8
		self.padding = numpy.zeros(((8 - ((self.count_7 * 60) % 8)) % 8), dtype='ubyte')
		self.set_defaults()

	def set_defaults(self):
		if self.context.version <= 32:
			self.zeros_start = numpy.zeros((6), dtype='ubyte')
		self.count_7 = 0
		self.zero = 0
		if self.context.version >= 48:
			self.zeros_pz = numpy.zeros((2), dtype='uint64')
		if self.context.version <= 32:
			self.unknown_list = Array(self.context)
		if self.context.version >= 47:
			self.unknown_list = Array(self.context)
		self.padding = numpy.zeros(((8 - ((self.count_7 * 60) % 8)) % 8), dtype='ubyte')

	def read(self, stream):
		self.io_start = stream.tell()
		if self.context.version <= 32:
			self.zeros_start = stream.read_ubytes((6))
		self.count_7 = stream.read_uint64()
		self.zero = stream.read_uint64()
		if self.context.version >= 48:
			self.zeros_pz = stream.read_uint64s((2))
		if self.context.version <= 32:
			self.unknown_list.read(stream, UACJoint, self.count_7, None)
		if self.context.version >= 47:
			self.unknown_list.read(stream, NasutoJointEntry, self.count_7, None)
		self.padding = stream.read_ubytes(((8 - ((self.count_7 * 60) % 8)) % 8))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		if self.context.version <= 32:
			stream.write_ubytes(self.zeros_start)
		stream.write_uint64(self.count_7)
		stream.write_uint64(self.zero)
		if self.context.version >= 48:
			stream.write_uint64s(self.zeros_pz)
		if self.context.version <= 32:
			self.unknown_list.write(stream, UACJoint, self.count_7, None)
		if self.context.version >= 47:
			self.unknown_list.write(stream, NasutoJointEntry, self.count_7, None)
		stream.write_ubytes(self.padding)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Struct7 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zeros_start = {self.zeros_start.__repr__()}'
		s += f'\n	* count_7 = {self.count_7.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		s += f'\n	* zeros_pz = {self.zeros_pz.__repr__()}'
		s += f'\n	* unknown_list = {self.unknown_list.__repr__()}'
		s += f'\n	* padding = {self.padding.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
