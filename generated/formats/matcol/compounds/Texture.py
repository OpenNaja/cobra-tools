import generated.formats.base.basic
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Texture(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# first fgm slot
		self.fgm_name = 0
		self.texture_suffix = 0
		self.texture_type = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.fgm_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.texture_suffix = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.texture_type = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.fgm_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.texture_suffix = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.texture_type = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.fgm_name.arg = 0
		instance.texture_suffix.arg = 0
		instance.texture_type.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.fgm_name)
		Pointer.to_stream(stream, instance.texture_suffix)
		Pointer.to_stream(stream, instance.texture_type)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('fgm_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('texture_suffix', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('texture_type', Pointer, (0, generated.formats.base.basic.ZString))

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
