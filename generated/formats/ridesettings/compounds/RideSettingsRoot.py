import generated.formats.ridesettings.compounds.Pair
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class RideSettingsRoot(MemStruct):

	__name__ = RideSettingsRoot

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_0 = 0.0
		self.unk_1 = 0
		self.count = 0
		self.pad_0 = 0
		self.pad_1 = 0
		self.pad_2 = 0
		self.array_1 = ArrayPointer(self.context, self.count, generated.formats.ridesettings.compounds.Pair.Pair)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.unk_0 = 0.0
		self.unk_1 = 0
		self.count = 0
		self.pad_0 = 0
		self.pad_1 = 0
		self.pad_2 = 0
		self.array_1 = ArrayPointer(self.context, self.count, generated.formats.ridesettings.compounds.Pair.Pair)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.unk_0 = Float.from_stream(stream, instance.context, 0, None)
		instance.unk_1 = Uint.from_stream(stream, instance.context, 0, None)
		instance.array_1 = ArrayPointer.from_stream(stream, instance.context, instance.count, generated.formats.ridesettings.compounds.Pair.Pair)
		instance.count = Uint.from_stream(stream, instance.context, 0, None)
		instance.pad_0 = Uint.from_stream(stream, instance.context, 0, None)
		instance.pad_1 = Uint.from_stream(stream, instance.context, 0, None)
		instance.pad_2 = Uint.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.array_1, int):
			instance.array_1.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Float.to_stream(stream, instance.unk_0)
		Uint.to_stream(stream, instance.unk_1)
		ArrayPointer.to_stream(stream, instance.array_1)
		Uint.to_stream(stream, instance.count)
		Uint.to_stream(stream, instance.pad_0)
		Uint.to_stream(stream, instance.pad_1)
		Uint.to_stream(stream, instance.pad_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'unk_0', Float, (0, None), (False, None)
		yield 'unk_1', Uint, (0, None), (False, None)
		yield 'array_1', ArrayPointer, (instance.count, generated.formats.ridesettings.compounds.Pair.Pair), (False, None)
		yield 'count', Uint, (0, None), (False, None)
		yield 'pad_0', Uint, (0, None), (False, None)
		yield 'pad_1', Uint, (0, None), (False, None)
		yield 'pad_2', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'RideSettingsRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* unk_0 = {self.fmt_member(self.unk_0, indent+1)}'
		s += f'\n	* unk_1 = {self.fmt_member(self.unk_1, indent+1)}'
		s += f'\n	* array_1 = {self.fmt_member(self.array_1, indent+1)}'
		s += f'\n	* count = {self.fmt_member(self.count, indent+1)}'
		s += f'\n	* pad_0 = {self.fmt_member(self.pad_0, indent+1)}'
		s += f'\n	* pad_1 = {self.fmt_member(self.pad_1, indent+1)}'
		s += f'\n	* pad_2 = {self.fmt_member(self.pad_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
