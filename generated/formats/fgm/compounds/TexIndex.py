from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class TexIndex(MemStruct):

	"""
	stores index into shader and array index of texture
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self._tex_index = 0

		# index of tile if an array texture is used eg JWE swatches
		self.array_index = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self._tex_index = 0
		if self.context.version >= 18:
			self.array_index = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance._tex_index = Uint.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 18:
			instance.array_index = Uint.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance._tex_index)
		if instance.context.version >= 18:
			stream.write_uint(instance.array_index)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield '_tex_index', Uint, (0, None)
		if instance.context.version >= 18:
			yield 'array_index', Uint, (0, None)

	def get_info_str(self, indent=0):
		return f'TexIndex [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* _tex_index = {self.fmt_member(self._tex_index, indent+1)}'
		s += f'\n	* array_index = {self.fmt_member(self.array_index, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
