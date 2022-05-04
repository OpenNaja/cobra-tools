from source.formats.base.basic import fmt_member
import numpy
from generated.array import Array
from generated.context import ContextReference
from generated.formats.bnk.compound.StreamInfo import StreamInfo


class BnkBufferData:

	"""
	Buffer data of bnk files
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# data size of aux file of type b
		self.size_b = 0

		# 1, guess
		self.buffer_count = 0

		# 1 for PC, 2 for PZ, JWE1, 6 for ZTUAC
		self.count_2 = 0

		# variable
		self.stream_info_count = 0

		# 0
		self.zeros = numpy.zeros((7,), dtype=numpy.dtype('uint32'))

		# variable
		self.zeros_per_buffer = numpy.zeros((self.buffer_count, 2,), dtype=numpy.dtype('uint64'))

		# data
		self.stream_infos = Array((self.stream_info_count,), StreamInfo, self.context, 0, None)

		# data
		self.name = ''

		# ext format subtypes
		self.external_b_suffix = ''

		# ext format subtypes
		self.external_s_suffix = ''
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.size_b = 0
		self.buffer_count = 0
		self.count_2 = 0
		self.stream_info_count = 0
		self.zeros = numpy.zeros((7,), dtype=numpy.dtype('uint32'))
		self.zeros_per_buffer = numpy.zeros((self.buffer_count, 2,), dtype=numpy.dtype('uint64'))
		self.stream_infos = Array((self.stream_info_count,), StreamInfo, self.context, 0, None)
		self.name = ''
		if self.buffer_count:
			self.external_b_suffix = ''
		if self.stream_info_count:
			self.external_s_suffix = ''

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		instance.size_b = stream.read_uint64()
		instance.buffer_count = stream.read_uint()
		instance.count_2 = stream.read_uint()
		instance.stream_info_count = stream.read_uint()
		instance.zeros = stream.read_uints((7,))
		instance.zeros_per_buffer = stream.read_uint64s((instance.buffer_count, 2,))
		instance.stream_infos = Array.from_stream(stream, (instance.stream_info_count,), StreamInfo, instance.context, 0, None)
		instance.name = stream.read_zstring()
		if instance.buffer_count:
			instance.external_b_suffix = stream.read_zstring()
		if instance.stream_info_count:
			instance.external_s_suffix = stream.read_zstring()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint64(instance.size_b)
		stream.write_uint(instance.buffer_count)
		stream.write_uint(instance.count_2)
		stream.write_uint(instance.stream_info_count)
		stream.write_uints(instance.zeros)
		stream.write_uint64s(instance.zeros_per_buffer)
		Array.to_stream(stream, instance.stream_infos, (instance.stream_info_count,), StreamInfo, instance.context, 0, None)
		stream.write_zstring(instance.name)
		if instance.buffer_count:
			stream.write_zstring(instance.external_b_suffix)
		if instance.stream_info_count:
			stream.write_zstring(instance.external_s_suffix)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'BnkBufferData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* size_b = {fmt_member(self.size_b, indent+1)}'
		s += f'\n	* buffer_count = {fmt_member(self.buffer_count, indent+1)}'
		s += f'\n	* count_2 = {fmt_member(self.count_2, indent+1)}'
		s += f'\n	* stream_info_count = {fmt_member(self.stream_info_count, indent+1)}'
		s += f'\n	* zeros = {fmt_member(self.zeros, indent+1)}'
		s += f'\n	* zeros_per_buffer = {fmt_member(self.zeros_per_buffer, indent+1)}'
		s += f'\n	* stream_infos = {fmt_member(self.stream_infos, indent+1)}'
		s += f'\n	* name = {fmt_member(self.name, indent+1)}'
		s += f'\n	* external_b_suffix = {fmt_member(self.external_b_suffix, indent+1)}'
		s += f'\n	* external_s_suffix = {fmt_member(self.external_s_suffix, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
