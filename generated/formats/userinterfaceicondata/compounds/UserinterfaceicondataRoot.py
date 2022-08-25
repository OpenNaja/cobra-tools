import generated.formats.base.basic
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class UserinterfaceicondataRoot(MemStruct):

	__name__ = UserinterfaceicondataRoot

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.tex_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.ovl_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.tex_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.ovl_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.tex_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.ovl_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		if not isinstance(instance.tex_name, int):
			instance.tex_name.arg = 0
		if not isinstance(instance.ovl_name, int):
			instance.ovl_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.tex_name)
		Pointer.to_stream(stream, instance.ovl_name)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'tex_name', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'ovl_name', Pointer, (0, generated.formats.base.basic.ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'UserinterfaceicondataRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* tex_name = {self.fmt_member(self.tex_name, indent+1)}'
		s += f'\n	* ovl_name = {self.fmt_member(self.ovl_name, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
