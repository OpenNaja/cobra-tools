from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64


class BufferGroup(BaseStruct):

	"""
	32 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# first buffer index
		self.buffer_offset = 0

		# number of buffers to grab
		self.buffer_count = 0

		# type of extension this entry is for
		self.ext_index = 0

		# which buffer index to populate
		self.buffer_index = 0

		# cumulative size of all buffers to grab
		self.size = 0

		# first data entry
		self.data_offset = 0

		# number of data entries to populate buffers into
		self.data_count = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.buffer_offset = 0
		self.buffer_count = 0
		self.ext_index = 0
		self.buffer_index = 0
		self.size = 0
		self.data_offset = 0
		self.data_count = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.buffer_offset = Uint.from_stream(stream, instance.context, 0, None)
		instance.buffer_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.ext_index = Uint.from_stream(stream, instance.context, 0, None)
		instance.buffer_index = Uint.from_stream(stream, instance.context, 0, None)
		instance.size = Uint64.from_stream(stream, instance.context, 0, None)
		instance.data_offset = Uint.from_stream(stream, instance.context, 0, None)
		instance.data_count = Uint.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.buffer_offset)
		Uint.to_stream(stream, instance.buffer_count)
		Uint.to_stream(stream, instance.ext_index)
		Uint.to_stream(stream, instance.buffer_index)
		Uint64.to_stream(stream, instance.size)
		Uint.to_stream(stream, instance.data_offset)
		Uint.to_stream(stream, instance.data_count)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'buffer_offset', Uint, (0, None)
		yield 'buffer_count', Uint, (0, None)
		yield 'ext_index', Uint, (0, None)
		yield 'buffer_index', Uint, (0, None)
		yield 'size', Uint64, (0, None)
		yield 'data_offset', Uint, (0, None)
		yield 'data_count', Uint, (0, None)

	def get_info_str(self, indent=0):
		return f'BufferGroup [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* buffer_offset = {self.fmt_member(self.buffer_offset, indent+1)}'
		s += f'\n	* buffer_count = {self.fmt_member(self.buffer_count, indent+1)}'
		s += f'\n	* ext_index = {self.fmt_member(self.ext_index, indent+1)}'
		s += f'\n	* buffer_index = {self.fmt_member(self.buffer_index, indent+1)}'
		s += f'\n	* size = {self.fmt_member(self.size, indent+1)}'
		s += f'\n	* data_offset = {self.fmt_member(self.data_offset, indent+1)}'
		s += f'\n	* data_count = {self.fmt_member(self.data_count, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
