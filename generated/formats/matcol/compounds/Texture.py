import generated.formats.base.basic
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Texture(MemStruct):

	__name__ = Texture

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# first fgm slot
		self.fgm_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.texture_suffix = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.texture_type = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.fgm_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.texture_suffix = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.texture_type = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.fgm_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.texture_suffix = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.texture_type = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		if not isinstance(instance.fgm_name, int):
			instance.fgm_name.arg = 0
		if not isinstance(instance.texture_suffix, int):
			instance.texture_suffix.arg = 0
		if not isinstance(instance.texture_type, int):
			instance.texture_type.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.fgm_name)
		Pointer.to_stream(stream, instance.texture_suffix)
		Pointer.to_stream(stream, instance.texture_type)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'fgm_name', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'texture_suffix', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'texture_type', Pointer, (0, generated.formats.base.basic.ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'Texture [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* fgm_name = {self.fmt_member(self.fgm_name, indent+1)}'
		s += f'\n	* texture_suffix = {self.fmt_member(self.texture_suffix, indent+1)}'
		s += f'\n	* texture_type = {self.fmt_member(self.texture_type, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
