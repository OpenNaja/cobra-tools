import numpy
from generated.array import Array
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.bnk.compound.StreamInfo import StreamInfo
from generated.struct import StructBase


class BnkBufferData(StructBase):

	"""
	Buffer data of bnk files
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# data size of aux file of type b
		self.size_b = 0

		# 1, guess
		self.buffer_count = 0

		# 1 for PC, 2 for PZ, JWE1, 6 for ZTUAC
		self.count_2 = 0

		# variable
		self.stream_info_count = 0

		# 0
		self.zeros = 0

		# variable
		self.zeros_per_buffer = 0

		# data
		self.stream_infos = 0

		# data
		self.name = 0

		# ext format subtypes
		self.external_b_suffix = 0

		# ext format subtypes
		self.external_s_suffix = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
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
		super().read_fields(stream, instance)
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
		super().write_fields(stream, instance)
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
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('size_b', Uint64, (0, None))
		yield ('buffer_count', Uint, (0, None))
		yield ('count_2', Uint, (0, None))
		yield ('stream_info_count', Uint, (0, None))
		yield ('zeros', Array, ((7,), Uint, 0, None))
		yield ('zeros_per_buffer', Array, ((instance.buffer_count, 2,), Uint64, 0, None))
		yield ('stream_infos', Array, ((instance.stream_info_count,), StreamInfo, 0, None))
		yield ('name', ZString, (0, None))
		if instance.buffer_count:
			yield ('external_b_suffix', ZString, (0, None))
		if instance.stream_info_count:
			yield ('external_s_suffix', ZString, (0, None))

	def get_info_str(self, indent=0):
		return f'BnkBufferData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* size_b = {self.fmt_member(self.size_b, indent+1)}'
		s += f'\n	* buffer_count = {self.fmt_member(self.buffer_count, indent+1)}'
		s += f'\n	* count_2 = {self.fmt_member(self.count_2, indent+1)}'
		s += f'\n	* stream_info_count = {self.fmt_member(self.stream_info_count, indent+1)}'
		s += f'\n	* zeros = {self.fmt_member(self.zeros, indent+1)}'
		s += f'\n	* zeros_per_buffer = {self.fmt_member(self.zeros_per_buffer, indent+1)}'
		s += f'\n	* stream_infos = {self.fmt_member(self.stream_infos, indent+1)}'
		s += f'\n	* name = {self.fmt_member(self.name, indent+1)}'
		s += f'\n	* external_b_suffix = {self.fmt_member(self.external_b_suffix, indent+1)}'
		s += f'\n	* external_s_suffix = {self.fmt_member(self.external_s_suffix, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
