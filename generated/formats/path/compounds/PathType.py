from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class PathType(MemStruct):

	__name__ = PathType

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.enum_value = 0
		self.min_width = 4.0
		self.max_width = 10.0
		self._unk_int_2 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.enum_value = 0
		self.min_width = 4.0
		self.max_width = 10.0
		self._unk_int_2 = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.enum_value = Uint.from_stream(stream, instance.context, 0, None)
		instance.min_width = Float.from_stream(stream, instance.context, 0, None)
		instance.max_width = Float.from_stream(stream, instance.context, 0, None)
		instance._unk_int_2 = Uint.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.enum_value)
		Float.to_stream(stream, instance.min_width)
		Float.to_stream(stream, instance.max_width)
		Uint.to_stream(stream, instance._unk_int_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'enum_value', Uint, (0, None), (False, None)
		yield 'min_width', Float, (0, None), (False, 4.0)
		yield 'max_width', Float, (0, None), (False, 10.0)
		yield '_unk_int_2', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'PathType [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* enum_value = {self.fmt_member(self.enum_value, indent+1)}'
		s += f'\n	* min_width = {self.fmt_member(self.min_width, indent+1)}'
		s += f'\n	* max_width = {self.fmt_member(self.max_width, indent+1)}'
		s += f'\n	* _unk_int_2 = {self.fmt_member(self._unk_int_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
