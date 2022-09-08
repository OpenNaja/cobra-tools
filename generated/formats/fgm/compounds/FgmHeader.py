from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
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
		self.textures = ArrayPointer(self.context, self._texture_count, FgmHeader._import_path_map["generated.formats.fgm.compounds.TextureInfo"])
		self.attributes = ArrayPointer(self.context, self._attribute_count, FgmHeader._import_path_map["generated.formats.fgm.compounds.AttribInfo"])
		self.name_foreach_textures = ForEachPointer(self.context, self.textures, FgmHeader._import_path_map["generated.formats.fgm.compounds.TextureData"])
		self.value_foreach_attributes = ForEachPointer(self.context, self.attributes, FgmHeader._import_path_map["generated.formats.fgm.compounds.AttribData"])
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
		self.textures = ArrayPointer(self.context, self._texture_count, FgmHeader._import_path_map["generated.formats.fgm.compounds.TextureInfo"])
		self.attributes = ArrayPointer(self.context, self._attribute_count, FgmHeader._import_path_map["generated.formats.fgm.compounds.AttribInfo"])
		self.name_foreach_textures = ForEachPointer(self.context, self.textures, FgmHeader._import_path_map["generated.formats.fgm.compounds.TextureData"])
		self.value_foreach_attributes = ForEachPointer(self.context, self.attributes, FgmHeader._import_path_map["generated.formats.fgm.compounds.AttribData"])

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version <= 15:
			yield '_texture_count', Uint, (0, None), (False, None)
		if instance.context.version >= 17:
			yield '_texture_count', Uint64, (0, None), (False, None)
		if instance.context.version <= 15:
			yield '_attribute_count', Uint, (0, None), (False, None)
		if instance.context.version >= 17:
			yield '_attribute_count', Uint64, (0, None), (False, None)
		yield 'textures', ArrayPointer, (instance._texture_count, FgmHeader._import_path_map["generated.formats.fgm.compounds.TextureInfo"]), (False, None)
		yield 'attributes', ArrayPointer, (instance._attribute_count, FgmHeader._import_path_map["generated.formats.fgm.compounds.AttribInfo"]), (False, None)
		yield 'name_foreach_textures', ForEachPointer, (instance.textures, FgmHeader._import_path_map["generated.formats.fgm.compounds.TextureData"]), (False, None)
		yield 'value_foreach_attributes', ForEachPointer, (instance.attributes, FgmHeader._import_path_map["generated.formats.fgm.compounds.AttribData"]), (False, None)
		yield '_unk_0', Uint64, (0, None), (False, None)
		yield '_unk_1', Uint64, (0, None), (False, None)
		if instance.context.user_version.is_jwe and (instance.context.version == 20):
			yield '_unk_2', Uint64, (0, None), (False, None)
			yield '_unk_3', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'FgmHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
