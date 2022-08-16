from generated.array import Array
from generated.formats.base.basic import Uint
from generated.formats.fgm.compounds.Color import Color
from generated.formats.fgm.compounds.GenericInfo import GenericInfo
from generated.formats.fgm.compounds.TexIndex import TexIndex


class TextureInfo(GenericInfo):

	"""
	part of fgm fragment, per texture involved
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Stores 2 rgba colors

		# Stores rgba color
		self.value = Array((1,), Color, self.context, 0, None)
		self.some_index_0 = 0
		self.some_index_1 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		if self.dtype == 8:
			self.value = Array((1,), TexIndex, self.context, 0, None)
		if self.context.version >= 18 and self.dtype == 7:
			self.value = Array((2,), Color, self.context, 0, None)
		if self.context.version <= 17 and self.dtype == 7:
			self.value = Array((1,), Color, self.context, 0, None)
		if self.context.version >= 18:
			self.some_index_0 = 0
			self.some_index_1 = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		if instance.dtype == 8:
			instance.value = Array.from_stream(stream, instance.context, 0, None, (1,), TexIndex)
		if instance.context.version >= 18 and instance.dtype == 7:
			instance.value = Array.from_stream(stream, instance.context, 0, None, (2,), Color)
		if instance.context.version <= 17 and instance.dtype == 7:
			instance.value = Array.from_stream(stream, instance.context, 0, None, (1,), Color)
		if instance.context.version >= 18:
			instance.some_index_0 = Uint.from_stream(stream, instance.context, 0, None)
			instance.some_index_1 = Uint.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.dtype == 8:
			Array.to_stream(stream, instance.value, (1,), TexIndex, instance.context, 0, None)
		if instance.context.version >= 18 and instance.dtype == 7:
			Array.to_stream(stream, instance.value, (2,), Color, instance.context, 0, None)
		if instance.context.version <= 17 and instance.dtype == 7:
			Array.to_stream(stream, instance.value, (1,), Color, instance.context, 0, None)
		if instance.context.version >= 18:
			Uint.to_stream(stream, instance.some_index_0)
			Uint.to_stream(stream, instance.some_index_1)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		if instance.dtype == 8:
			yield 'value', Array, ((1,), TexIndex, 0, None), (False, None)
		if instance.context.version >= 18 and instance.dtype == 7:
			yield 'value', Array, ((2,), Color, 0, None), (False, None)
		if instance.context.version <= 17 and instance.dtype == 7:
			yield 'value', Array, ((1,), Color, 0, None), (False, None)
		if instance.context.version >= 18:
			yield 'some_index_0', Uint, (0, None), (True, 0)
			yield 'some_index_1', Uint, (0, None), (True, 0)

	def get_info_str(self, indent=0):
		return f'TextureInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* value = {self.fmt_member(self.value, indent+1)}'
		s += f'\n	* some_index_0 = {self.fmt_member(self.some_index_0, indent+1)}'
		s += f'\n	* some_index_1 = {self.fmt_member(self.some_index_1, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
