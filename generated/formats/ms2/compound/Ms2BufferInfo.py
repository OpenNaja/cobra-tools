import numpy
import typing
from generated.array import Array


class Ms2BufferInfo:

	"""
	Fragment data describing a MS2 buffer giving the size of the whole vertex and tri buffer.
	JWE: 48 bytes
	PZ: 56 bytes
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# JWE, 16 bytes of 00 padding
		self.skip_1 = numpy.zeros((4), dtype='uint')
		self.vertexdatasize = 0

		# 8 empty bytes
		self.ptr_1 = 0

		# PZ, another 8 empty bytes
		self.unk_0 = 0
		self.facesdatasize = 0

		# 8 empty bytes
		self.ptr_2 = 0

		# PZ, another 16 empty bytes
		self.unk_2 = numpy.zeros((2), dtype='uint64')

	def read(self, stream):

		self.io_start = stream.tell()
		if ((stream.user_version == 24724) or (stream.user_version == 25108)) and (stream.version == 19):
			self.skip_1 = stream.read_uints((4))
		self.vertexdatasize = stream.read_uint64()
		self.ptr_1 = stream.read_uint64()
		if ((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version == 19):
			self.unk_0 = stream.read_uint64()
		self.facesdatasize = stream.read_uint64()
		self.ptr_2 = stream.read_uint64()
		if ((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version == 19):
			self.unk_2 = stream.read_uint64s((2))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		if ((stream.user_version == 24724) or (stream.user_version == 25108)) and (stream.version == 19):
			stream.write_uints(self.skip_1)
		stream.write_uint64(self.vertexdatasize)
		stream.write_uint64(self.ptr_1)
		if ((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version == 19):
			stream.write_uint64(self.unk_0)
		stream.write_uint64(self.facesdatasize)
		stream.write_uint64(self.ptr_2)
		if ((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version == 19):
			stream.write_uint64s(self.unk_2)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Ms2BufferInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* skip_1 = {self.skip_1.__repr__()}'
		s += f'\n	* vertexdatasize = {self.vertexdatasize.__repr__()}'
		s += f'\n	* ptr_1 = {self.ptr_1.__repr__()}'
		s += f'\n	* unk_0 = {self.unk_0.__repr__()}'
		s += f'\n	* facesdatasize = {self.facesdatasize.__repr__()}'
		s += f'\n	* ptr_2 = {self.ptr_2.__repr__()}'
		s += f'\n	* unk_2 = {self.unk_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
