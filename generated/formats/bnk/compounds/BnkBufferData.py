import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.bnk.compounds.StreamInfo import StreamInfo


class BnkBufferData(BaseStruct):

	"""
	Buffer data of bnk files
	"""

	__name__ = BnkBufferData

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
		self.zeros = Array((0,), Uint, self.context, 0, None)

		# variable
		self.zeros_per_buffer = Array((0,), Uint64, self.context, 0, None)

		# data
		self.stream_infos = Array((0,), StreamInfo, self.context, 0, None)

		# data
		self.name = ''

		# ext format subtypes
		self.external_b_suffix = ''

		# ext format subtypes
		self.external_s_suffix = ''
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
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

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.size_b = Uint64.from_stream(stream, instance.context, 0, None)
		instance.buffer_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.count_2 = Uint.from_stream(stream, instance.context, 0, None)
		instance.stream_info_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.zeros = Array.from_stream(stream, instance.context, 0, None, (7,), Uint)
		instance.zeros_per_buffer = Array.from_stream(stream, instance.context, 0, None, (instance.buffer_count, 2,), Uint64)
		instance.stream_infos = Array.from_stream(stream, instance.context, 0, None, (instance.stream_info_count,), StreamInfo)
		instance.name = ZString.from_stream(stream, instance.context, 0, None)
		if instance.buffer_count:
			instance.external_b_suffix = ZString.from_stream(stream, instance.context, 0, None)
		if instance.stream_info_count:
			instance.external_s_suffix = ZString.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.size_b)
		Uint.to_stream(stream, instance.buffer_count)
		Uint.to_stream(stream, instance.count_2)
		Uint.to_stream(stream, instance.stream_info_count)
		Array.to_stream(stream, instance.zeros, (7,), Uint, instance.context, 0, None)
		Array.to_stream(stream, instance.zeros_per_buffer, (instance.buffer_count, 2,), Uint64, instance.context, 0, None)
		Array.to_stream(stream, instance.stream_infos, (instance.stream_info_count,), StreamInfo, instance.context, 0, None)
		ZString.to_stream(stream, instance.name)
		if instance.buffer_count:
			ZString.to_stream(stream, instance.external_b_suffix)
		if instance.stream_info_count:
			ZString.to_stream(stream, instance.external_s_suffix)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'size_b', Uint64, (0, None), (False, None)
		yield 'buffer_count', Uint, (0, None), (False, None)
		yield 'count_2', Uint, (0, None), (False, None)
		yield 'stream_info_count', Uint, (0, None), (False, None)
		yield 'zeros', Array, ((7,), Uint, 0, None), (False, None)
		yield 'zeros_per_buffer', Array, ((instance.buffer_count, 2,), Uint64, 0, None), (False, None)
		yield 'stream_infos', Array, ((instance.stream_info_count,), StreamInfo, 0, None), (False, None)
		yield 'name', ZString, (0, None), (False, None)
		if instance.buffer_count:
			yield 'external_b_suffix', ZString, (0, None), (False, None)
		if instance.stream_info_count:
			yield 'external_s_suffix', ZString, (0, None), (False, None)

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
