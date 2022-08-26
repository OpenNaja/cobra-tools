from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class FontInfo(MemStruct):

	"""
	24 bytes
	"""

	__name__ = 'FontInfo'

	_import_path = 'generated.formats.scaleformlanguagedata.compounds.FontInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.flag_or_count = 0
		self.style_name = Pointer(self.context, 0, ZString)
		self.font_file = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.flag_or_count = 0
		self.style_name = Pointer(self.context, 0, ZString)
		self.font_file = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.style_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.font_file = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.flag_or_count = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.style_name, int):
			instance.style_name.arg = 0
		if not isinstance(instance.font_file, int):
			instance.font_file.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.style_name)
		Pointer.to_stream(stream, instance.font_file)
		Uint64.to_stream(stream, instance.flag_or_count)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'style_name', Pointer, (0, ZString), (False, None)
		yield 'font_file', Pointer, (0, ZString), (False, None)
		yield 'flag_or_count', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'FontInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* style_name = {self.fmt_member(self.style_name, indent+1)}'
		s += f'\n	* font_file = {self.fmt_member(self.font_file, indent+1)}'
		s += f'\n	* flag_or_count = {self.fmt_member(self.flag_or_count, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
