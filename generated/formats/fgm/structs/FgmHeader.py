from generated.formats.fgm.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class FgmHeader(MemStruct):

	"""
	# JWE, PZ - 64 bytes
	# JWE2, PC2 - 80 bytes
	# JWE2 patternset fgms seem to be in pool type 3, everything else in 2
	"""

	__name__ = 'FgmHeader'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.textures_count = name_type_map['Uint64'](self.context, 0, None)
		self.attributes_count = name_type_map['Uint64'](self.context, 0, None)
		self.unk_0 = name_type_map['Uint64'].from_value(0)
		self.unk_1 = name_type_map['Uint64'].from_value(0)
		self.unk_2 = name_type_map['Uint64'].from_value(0)
		self.unk_3 = name_type_map['Uint64'].from_value(0)
		self.textures = name_type_map['ArrayPointer'](self.context, self.textures_count, name_type_map['TextureInfo'])
		self.attributes = name_type_map['ArrayPointer'](self.context, self.attributes_count, name_type_map['AttribInfo'])
		self.name_foreach_textures = name_type_map['ForEachPointer'](self.context, self.textures, name_type_map['TextureData'])
		self.value_foreach_attributes = name_type_map['ForEachPointer'](self.context, self.attributes, name_type_map['AttribData'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'textures_count', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version <= 15, None)
		yield 'textures_count', name_type_map['Uint64'], (0, None), (False, None), (lambda context: context.version >= 17, None)
		yield 'attributes_count', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version <= 15, None)
		yield 'attributes_count', name_type_map['Uint64'], (0, None), (False, None), (lambda context: context.version >= 17, None)
		yield 'textures', name_type_map['ArrayPointer'], (None, name_type_map['TextureInfo']), (False, None), (None, None)
		yield 'attributes', name_type_map['ArrayPointer'], (None, name_type_map['AttribInfo']), (False, None), (None, None)
		yield 'name_foreach_textures', name_type_map['ForEachPointer'], (None, name_type_map['TextureData']), (False, None), (None, None)
		yield 'value_foreach_attributes', name_type_map['ForEachPointer'], (None, name_type_map['AttribData']), (False, None), (None, None)
		yield 'unk_0', name_type_map['Uint64'], (0, None), (True, 0), (None, None)
		yield 'unk_1', name_type_map['Uint64'], (0, None), (True, 0), (None, None)
		yield 'unk_2', name_type_map['Uint64'], (0, None), (True, 0), (lambda context: (context.user_version.use_djb and (context.version == 20)) or (context.mime_version == 7), None)
		yield 'unk_3', name_type_map['Uint64'], (0, None), (True, 0), (lambda context: (context.user_version.use_djb and (context.version == 20)) or (context.mime_version == 7), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version <= 15:
			yield 'textures_count', name_type_map['Uint'], (0, None), (False, None)
		if instance.context.version >= 17:
			yield 'textures_count', name_type_map['Uint64'], (0, None), (False, None)
		if instance.context.version <= 15:
			yield 'attributes_count', name_type_map['Uint'], (0, None), (False, None)
		if instance.context.version >= 17:
			yield 'attributes_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'textures', name_type_map['ArrayPointer'], (instance.textures_count, name_type_map['TextureInfo']), (False, None)
		yield 'attributes', name_type_map['ArrayPointer'], (instance.attributes_count, name_type_map['AttribInfo']), (False, None)
		yield 'name_foreach_textures', name_type_map['ForEachPointer'], (instance.textures, name_type_map['TextureData']), (False, None)
		yield 'value_foreach_attributes', name_type_map['ForEachPointer'], (instance.attributes, name_type_map['AttribData']), (False, None)
		yield 'unk_0', name_type_map['Uint64'], (0, None), (True, 0)
		yield 'unk_1', name_type_map['Uint64'], (0, None), (True, 0)
		if (instance.context.user_version.use_djb and (instance.context.version == 20)) or (instance.context.mime_version == 7):
			yield 'unk_2', name_type_map['Uint64'], (0, None), (True, 0)
			yield 'unk_3', name_type_map['Uint64'], (0, None), (True, 0)
