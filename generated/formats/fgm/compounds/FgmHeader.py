from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.fgm.compounds.AttribData import AttribData
from generated.formats.fgm.compounds.AttribInfo import AttribInfo
from generated.formats.fgm.compounds.TextureData import TextureData
from generated.formats.fgm.compounds.TextureInfo import TextureInfo
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.ForEachPointer import ForEachPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class FgmHeader(MemStruct):

	"""
	# JWE1, PZ - 64 bytes
	# JWE2 - 80 bytes
	# JWE2 patternset fgms seem to be in pool type 3, everything else in 2
	"""

	__name__ = 'FgmHeader'

	_import_path = 'generated.formats.fgm.compounds.FgmHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self._texture_count = 0
		self._attribute_count = 0
		self._unk_0 = 0
		self._unk_1 = 0
		self._unk_2 = 0
		self._unk_3 = 0
		self.textures = ArrayPointer(self.context, self._texture_count, TextureInfo)
		self.attributes = ArrayPointer(self.context, self._attribute_count, AttribInfo)
		self.name_foreach_textures = ForEachPointer(self.context, self.textures, TextureData)
		self.value_foreach_attributes = ForEachPointer(self.context, self.attributes, AttribData)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		if self.context.version <= 15:
			self._texture_count = 0
		if self.context.version >= 17:
			self._texture_count = 0
		if self.context.version <= 15:
			self._attribute_count = 0
		if self.context.version >= 17:
			self._attribute_count = 0
		self._unk_0 = 0
		self._unk_1 = 0
		if self.context.user_version.is_jwe and (self.context.version == 20):
			self._unk_2 = 0
			self._unk_3 = 0
		self.textures = ArrayPointer(self.context, self._texture_count, TextureInfo)
		self.attributes = ArrayPointer(self.context, self._attribute_count, AttribInfo)
		self.name_foreach_textures = ForEachPointer(self.context, self.textures, TextureData)
		self.value_foreach_attributes = ForEachPointer(self.context, self.attributes, AttribData)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		if instance.context.version <= 15:
			instance._texture_count = Uint.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 17:
			instance._texture_count = Uint64.from_stream(stream, instance.context, 0, None)
		if instance.context.version <= 15:
			instance._attribute_count = Uint.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 17:
			instance._attribute_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.textures = ArrayPointer.from_stream(stream, instance.context, instance._texture_count, TextureInfo)
		instance.attributes = ArrayPointer.from_stream(stream, instance.context, instance._attribute_count, AttribInfo)
		instance.name_foreach_textures = ForEachPointer.from_stream(stream, instance.context, instance.textures, TextureData)
		instance.value_foreach_attributes = ForEachPointer.from_stream(stream, instance.context, instance.attributes, AttribData)
		instance._unk_0 = Uint64.from_stream(stream, instance.context, 0, None)
		instance._unk_1 = Uint64.from_stream(stream, instance.context, 0, None)
		if instance.context.user_version.is_jwe and (instance.context.version == 20):
			instance._unk_2 = Uint64.from_stream(stream, instance.context, 0, None)
			instance._unk_3 = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.textures, int):
			instance.textures.arg = instance._texture_count
		if not isinstance(instance.attributes, int):
			instance.attributes.arg = instance._attribute_count
		if not isinstance(instance.name_foreach_textures, int):
			instance.name_foreach_textures.arg = instance.textures
		if not isinstance(instance.value_foreach_attributes, int):
			instance.value_foreach_attributes.arg = instance.attributes

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.context.version <= 15:
			Uint.to_stream(stream, instance._texture_count)
		if instance.context.version >= 17:
			Uint64.to_stream(stream, instance._texture_count)
		if instance.context.version <= 15:
			Uint.to_stream(stream, instance._attribute_count)
		if instance.context.version >= 17:
			Uint64.to_stream(stream, instance._attribute_count)
		ArrayPointer.to_stream(stream, instance.textures)
		ArrayPointer.to_stream(stream, instance.attributes)
		ForEachPointer.to_stream(stream, instance.name_foreach_textures)
		ForEachPointer.to_stream(stream, instance.value_foreach_attributes)
		Uint64.to_stream(stream, instance._unk_0)
		Uint64.to_stream(stream, instance._unk_1)
		if instance.context.user_version.is_jwe and (instance.context.version == 20):
			Uint64.to_stream(stream, instance._unk_2)
			Uint64.to_stream(stream, instance._unk_3)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		if instance.context.version <= 15:
			yield '_texture_count', Uint, (0, None), (False, None)
		if instance.context.version >= 17:
			yield '_texture_count', Uint64, (0, None), (False, None)
		if instance.context.version <= 15:
			yield '_attribute_count', Uint, (0, None), (False, None)
		if instance.context.version >= 17:
			yield '_attribute_count', Uint64, (0, None), (False, None)
		yield 'textures', ArrayPointer, (instance._texture_count, TextureInfo), (False, None)
		yield 'attributes', ArrayPointer, (instance._attribute_count, AttribInfo), (False, None)
		yield 'name_foreach_textures', ForEachPointer, (instance.textures, TextureData), (False, None)
		yield 'value_foreach_attributes', ForEachPointer, (instance.attributes, AttribData), (False, None)
		yield '_unk_0', Uint64, (0, None), (False, None)
		yield '_unk_1', Uint64, (0, None), (False, None)
		if instance.context.user_version.is_jwe and (instance.context.version == 20):
			yield '_unk_2', Uint64, (0, None), (False, None)
			yield '_unk_3', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'FgmHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* _texture_count = {self.fmt_member(self._texture_count, indent+1)}'
		s += f'\n	* _attribute_count = {self.fmt_member(self._attribute_count, indent+1)}'
		s += f'\n	* textures = {self.fmt_member(self.textures, indent+1)}'
		s += f'\n	* attributes = {self.fmt_member(self.attributes, indent+1)}'
		s += f'\n	* name_foreach_textures = {self.fmt_member(self.name_foreach_textures, indent+1)}'
		s += f'\n	* value_foreach_attributes = {self.fmt_member(self.value_foreach_attributes, indent+1)}'
		s += f'\n	* _unk_0 = {self.fmt_member(self._unk_0, indent+1)}'
		s += f'\n	* _unk_1 = {self.fmt_member(self._unk_1, indent+1)}'
		s += f'\n	* _unk_2 = {self.fmt_member(self._unk_2, indent+1)}'
		s += f'\n	* _unk_3 = {self.fmt_member(self._unk_3, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
