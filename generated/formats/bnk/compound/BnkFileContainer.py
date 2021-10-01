import numpy
import typing
from generated.array import Array
from generated.context import ContextReference


class BnkFileContainer:

	"""
	Buffer data of bnk files
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# data size of aux file of type b
		self.size_b = 0

		# 1, guess
		self.name_count = 0

		# 2 for PZ, 6 for ZTUAC
		self.unk = 0

		# variable
		self.stream_info_count = 0

		# 0
		self.zeros = numpy.zeros((11), dtype='uint')

		# data
		self.stream_infos = numpy.zeros((self.stream_info_count, 3), dtype='uint64')

		# data
		self.names = Array(self.context)

		# ext format subtypes
		self.extensions = Array(self.context)
		self.set_defaults()

	def set_defaults(self):
		self.size_b = 0
		self.name_count = 0
		self.unk = 0
		self.stream_info_count = 0
		self.zeros = numpy.zeros((11), dtype='uint')
		self.stream_infos = numpy.zeros((self.stream_info_count, 3), dtype='uint64')
		self.names = Array(self.context)
		self.extensions = Array(self.context)

	def read(self, stream):
		self.io_start = stream.tell()
		self.size_b = stream.read_uint64()
		self.name_count = stream.read_uint()
		self.unk = stream.read_uint()
		self.stream_info_count = stream.read_uint()
		self.zeros = stream.read_uints((11))
		self.stream_infos = stream.read_uint64s((self.stream_info_count, 3))
		self.names = stream.read_zstrings((self.name_count))
		self.extensions = stream.read_zstrings((2))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64(self.size_b)
		stream.write_uint(self.name_count)
		stream.write_uint(self.unk)
		stream.write_uint(self.stream_info_count)
		stream.write_uints(self.zeros)
		stream.write_uint64s(self.stream_infos)
		stream.write_zstrings(self.names)
		stream.write_zstrings(self.extensions)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'BnkFileContainer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* size_b = {self.size_b.__repr__()}'
		s += f'\n	* name_count = {self.name_count.__repr__()}'
		s += f'\n	* unk = {self.unk.__repr__()}'
		s += f'\n	* stream_info_count = {self.stream_info_count.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* stream_infos = {self.stream_infos.__repr__()}'
		s += f'\n	* names = {self.names.__repr__()}'
		s += f'\n	* extensions = {self.extensions.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
