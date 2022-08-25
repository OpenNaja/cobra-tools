import generated.formats.lut.compounds.Vector3
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class LutHeader(MemStruct):

	"""
	24 bytes for JWE2
	"""

	__name__ = 'LutHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.colors_count = 0
		self.unk_0 = 0
		self.unk_1 = 0
		self.colors_in_column_count = 0
		self.unk_2 = 0
		self.colors = ArrayPointer(self.context, self.colors_count, generated.formats.lut.compounds.Vector3.Vector3)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.colors_count = 0
		self.unk_0 = 0
		self.unk_1 = 0
		self.colors_in_column_count = 0
		self.unk_2 = 0
		self.colors = ArrayPointer(self.context, self.colors_count, generated.formats.lut.compounds.Vector3.Vector3)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.colors = ArrayPointer.from_stream(stream, instance.context, instance.colors_count, generated.formats.lut.compounds.Vector3.Vector3)
		instance.colors_count = Ushort.from_stream(stream, instance.context, 0, None)
		instance.unk_0 = Ushort.from_stream(stream, instance.context, 0, None)
		instance.unk_1 = Uint.from_stream(stream, instance.context, 0, None)
		instance.colors_in_column_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.unk_2 = Uint.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.colors, int):
			instance.colors.arg = instance.colors_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		ArrayPointer.to_stream(stream, instance.colors)
		Ushort.to_stream(stream, instance.colors_count)
		Ushort.to_stream(stream, instance.unk_0)
		Uint.to_stream(stream, instance.unk_1)
		Uint.to_stream(stream, instance.colors_in_column_count)
		Uint.to_stream(stream, instance.unk_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'colors', ArrayPointer, (instance.colors_count, generated.formats.lut.compounds.Vector3.Vector3), (False, None)
		yield 'colors_count', Ushort, (0, None), (False, None)
		yield 'unk_0', Ushort, (0, None), (False, None)
		yield 'unk_1', Uint, (0, None), (False, None)
		yield 'colors_in_column_count', Uint, (0, None), (False, None)
		yield 'unk_2', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'LutHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* colors = {self.fmt_member(self.colors, indent+1)}'
		s += f'\n	* colors_count = {self.fmt_member(self.colors_count, indent+1)}'
		s += f'\n	* unk_0 = {self.fmt_member(self.unk_0, indent+1)}'
		s += f'\n	* unk_1 = {self.fmt_member(self.unk_1, indent+1)}'
		s += f'\n	* colors_in_column_count = {self.fmt_member(self.colors_in_column_count, indent+1)}'
		s += f'\n	* unk_2 = {self.fmt_member(self.unk_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
