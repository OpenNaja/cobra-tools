import generated.formats.base.basic
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class StringData(MemStruct):

	"""
	16 bytes in log
	"""

	__name__ = StringData

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ioptional = 0
		self.str_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.ioptional = 0
		self.str_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.str_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.ioptional = Uint.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.str_name, int):
			instance.str_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.str_name)
		Uint.to_stream(stream, instance.ioptional)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'str_name', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'ioptional', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'StringData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* str_name = {self.fmt_member(self.str_name, indent+1)}'
		s += f'\n	* ioptional = {self.fmt_member(self.ioptional, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
