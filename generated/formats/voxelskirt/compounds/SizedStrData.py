from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint64


class SizedStrData(BaseStruct):

	"""
	# size varies according to game
	"""

	__name__ = 'SizedStrData'

	_import_path = 'generated.formats.voxelskirt.compounds.SizedStrData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zero = 0

		# total size of buffer data
		self.data_size = 0
		self.x = 0
		self.y = 0
		self.scale = 0.0
		self.padding = 0.0

		# zero, for PC only
		self.zero_pc = 0

		# x*y*4, for PC only
		self.height_array_size_pc = 0
		self.data_offset = 0

		# entries of 32 bytes
		self.data_count = 0
		self.size_offset = 0

		# entries of 40 bytes
		self.size_count = 0

		# slightly smaller than total size of buffer data
		self.position_offset = 0

		# counts the -1 structs; entries of 32 bytes
		self.position_count = 0

		# offset into buffer to start of sth; only given if some count is nonzero
		self.mat_offset = 0
		self.mat_count = 0

		# offset into buffer to start of name zstrings
		self.name_buffer_offset = 0

		# also counts the stuff after names
		self.name_count = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.zero = 0
		self.data_size = 0
		self.x = 0
		self.y = 0
		self.scale = 0.0
		self.padding = 0.0
		if self.context.version == 18:
			self.zero_pc = 0
			self.height_array_size_pc = 0
		if not (self.context.version == 18):
			self.data_offset = 0
			self.data_count = 0
			self.size_offset = 0
			self.size_count = 0
		self.position_offset = 0
		self.position_count = 0
		self.mat_offset = 0
		self.mat_count = 0
		self.name_buffer_offset = 0
		self.name_count = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.zero = Uint64.from_stream(stream, instance.context, 0, None)
		instance.data_size = Uint64.from_stream(stream, instance.context, 0, None)
		instance.x = Uint64.from_stream(stream, instance.context, 0, None)
		instance.y = Uint64.from_stream(stream, instance.context, 0, None)
		instance.scale = Float.from_stream(stream, instance.context, 0, None)
		instance.padding = Float.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 18:
			instance.zero_pc = Uint64.from_stream(stream, instance.context, 0, None)
			instance.height_array_size_pc = Uint64.from_stream(stream, instance.context, 0, None)
		if not (instance.context.version == 18):
			instance.data_offset = Uint64.from_stream(stream, instance.context, 0, None)
			instance.data_count = Uint64.from_stream(stream, instance.context, 0, None)
			instance.size_offset = Uint64.from_stream(stream, instance.context, 0, None)
			instance.size_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.position_offset = Uint64.from_stream(stream, instance.context, 0, None)
		instance.position_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.mat_offset = Uint64.from_stream(stream, instance.context, 0, None)
		instance.mat_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.name_buffer_offset = Uint64.from_stream(stream, instance.context, 0, None)
		instance.name_count = Uint64.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.zero)
		Uint64.to_stream(stream, instance.data_size)
		Uint64.to_stream(stream, instance.x)
		Uint64.to_stream(stream, instance.y)
		Float.to_stream(stream, instance.scale)
		Float.to_stream(stream, instance.padding)
		if instance.context.version == 18:
			Uint64.to_stream(stream, instance.zero_pc)
			Uint64.to_stream(stream, instance.height_array_size_pc)
		if not (instance.context.version == 18):
			Uint64.to_stream(stream, instance.data_offset)
			Uint64.to_stream(stream, instance.data_count)
			Uint64.to_stream(stream, instance.size_offset)
			Uint64.to_stream(stream, instance.size_count)
		Uint64.to_stream(stream, instance.position_offset)
		Uint64.to_stream(stream, instance.position_count)
		Uint64.to_stream(stream, instance.mat_offset)
		Uint64.to_stream(stream, instance.mat_count)
		Uint64.to_stream(stream, instance.name_buffer_offset)
		Uint64.to_stream(stream, instance.name_count)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'zero', Uint64, (0, None), (False, None)
		yield 'data_size', Uint64, (0, None), (False, None)
		yield 'x', Uint64, (0, None), (False, None)
		yield 'y', Uint64, (0, None), (False, None)
		yield 'scale', Float, (0, None), (False, None)
		yield 'padding', Float, (0, None), (False, None)
		if instance.context.version == 18:
			yield 'zero_pc', Uint64, (0, None), (False, None)
			yield 'height_array_size_pc', Uint64, (0, None), (False, None)
		if not (instance.context.version == 18):
			yield 'data_offset', Uint64, (0, None), (False, None)
			yield 'data_count', Uint64, (0, None), (False, None)
			yield 'size_offset', Uint64, (0, None), (False, None)
			yield 'size_count', Uint64, (0, None), (False, None)
		yield 'position_offset', Uint64, (0, None), (False, None)
		yield 'position_count', Uint64, (0, None), (False, None)
		yield 'mat_offset', Uint64, (0, None), (False, None)
		yield 'mat_count', Uint64, (0, None), (False, None)
		yield 'name_buffer_offset', Uint64, (0, None), (False, None)
		yield 'name_count', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'SizedStrData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* zero = {self.fmt_member(self.zero, indent+1)}'
		s += f'\n	* data_size = {self.fmt_member(self.data_size, indent+1)}'
		s += f'\n	* x = {self.fmt_member(self.x, indent+1)}'
		s += f'\n	* y = {self.fmt_member(self.y, indent+1)}'
		s += f'\n	* scale = {self.fmt_member(self.scale, indent+1)}'
		s += f'\n	* padding = {self.fmt_member(self.padding, indent+1)}'
		s += f'\n	* zero_pc = {self.fmt_member(self.zero_pc, indent+1)}'
		s += f'\n	* height_array_size_pc = {self.fmt_member(self.height_array_size_pc, indent+1)}'
		s += f'\n	* data_offset = {self.fmt_member(self.data_offset, indent+1)}'
		s += f'\n	* data_count = {self.fmt_member(self.data_count, indent+1)}'
		s += f'\n	* size_offset = {self.fmt_member(self.size_offset, indent+1)}'
		s += f'\n	* size_count = {self.fmt_member(self.size_count, indent+1)}'
		s += f'\n	* position_offset = {self.fmt_member(self.position_offset, indent+1)}'
		s += f'\n	* position_count = {self.fmt_member(self.position_count, indent+1)}'
		s += f'\n	* mat_offset = {self.fmt_member(self.mat_offset, indent+1)}'
		s += f'\n	* mat_count = {self.fmt_member(self.mat_count, indent+1)}'
		s += f'\n	* name_buffer_offset = {self.fmt_member(self.name_buffer_offset, indent+1)}'
		s += f'\n	* name_count = {self.fmt_member(self.name_count, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
