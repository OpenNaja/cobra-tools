from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Texture(MemStruct):

	__name__ = 'Texture'

	_import_path = 'generated.formats.matcol.compounds.Texture'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# first fgm slot
		self.fgm_name = Pointer(self.context, 0, ZString)
		self.texture_suffix = Pointer(self.context, 0, ZString)
		self.texture_type = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.fgm_name = Pointer(self.context, 0, ZString)
		self.texture_suffix = Pointer(self.context, 0, ZString)
		self.texture_type = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.fgm_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.texture_suffix = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.texture_type = Pointer.from_stream(stream, instance.context, 0, ZString)
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
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'fgm_name', Pointer, (0, ZString), (False, None)
		yield 'texture_suffix', Pointer, (0, ZString), (False, None)
		yield 'texture_type', Pointer, (0, ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'Texture [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
