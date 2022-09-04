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

	__name__ = 'BnkBufferData'

	_import_path = 'generated.formats.bnk.compounds.BnkBufferData'

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
		self.zeros = Array(self.context, 0, None, (0,), Uint)

		# variable
		self.zeros_per_buffer = Array(self.context, 0, None, (0,), Uint64)

		# data
		self.stream_infos = Array(self.context, 0, None, (0,), StreamInfo)

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
		self.stream_infos = Array(self.context, 0, None, (self.stream_info_count,), StreamInfo)
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
		Array.to_stream(stream, instance.zeros, instance.context, 0, None, (7,), Uint)
		Array.to_stream(stream, instance.zeros_per_buffer, instance.context, 0, None, (instance.buffer_count, 2,), Uint64)
		Array.to_stream(stream, instance.stream_infos, instance.context, 0, None, (instance.stream_info_count,), StreamInfo)
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
		yield 'zeros', Array, (0, None, (7,), Uint), (False, None)
		yield 'zeros_per_buffer', Array, (0, None, (instance.buffer_count, 2,), Uint64), (False, None)
		yield 'stream_infos', Array, (0, None, (instance.stream_info_count,), StreamInfo), (False, None)
		yield 'name', ZString, (0, None), (False, None)
		if instance.buffer_count:
			yield 'external_b_suffix', ZString, (0, None), (False, None)
		if instance.stream_info_count:
			yield 'external_s_suffix', ZString, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'BnkBufferData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
