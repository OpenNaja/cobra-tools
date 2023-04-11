from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.particleeffect.imports import name_type_map


class ParticleEffectRoot(MemStruct):

	__name__ = 'ParticleEffectRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_64_1 = name_type_map['Uint64'](self.context, 0, None)
		self.unk_64_2 = name_type_map['Uint64'](self.context, 0, None)
		self.unk_64_3 = name_type_map['Uint64'](self.context, 0, None)
		self.unk_64_4 = name_type_map['Uint64'](self.context, 0, None)
		self.unk_64_5 = name_type_map['Uint64'](self.context, 0, None)
		self.unk_64_6 = name_type_map['Uint64'](self.context, 0, None)
		self.unk_32_1 = name_type_map['Uint'](self.context, 0, None)
		self.unk_32_2_neg = name_type_map['Int'](self.context, 0, None)
		self.unk_32_3 = name_type_map['Uint'](self.context, 0, None)
		self.unk_32_4 = name_type_map['Uint'](self.context, 0, None)
		self.a_unk_32_1 = name_type_map['Uint'](self.context, 0, None)
		self.a_unk_32_2 = name_type_map['Uint'](self.context, 0, None)
		self.a_unk_32_3_1 = name_type_map['Uint'](self.context, 0, None)
		self.a_unk_32_4 = name_type_map['Uint'](self.context, 0, None)
		self.atlasinfo_count = name_type_map['Uint64'](self.context, 0, None)
		self.next_row_1 = name_type_map['NextRow1'](self.context, 0, None)
		self.next_row_2 = name_type_map['NextRow2'](self.context, 0, None)
		self.next_row_3 = name_type_map['NextRow2'](self.context, 0, None)
		self.next_row_4 = name_type_map['NextRow2'](self.context, 0, None)
		self.next_row_5 = name_type_map['LastRow'](self.context, 0, None)
		self.name_foreach_textures = name_type_map['ArrayPointer'](self.context, self.atlasinfo_count, name_type_map['TextureData'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'unk_64_1', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_64_2', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_64_3', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_64_4', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_64_5', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_64_6', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_32_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_32_2_neg', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'unk_32_3', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_32_4', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'a_unk_32_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'a_unk_32_2', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'a_unk_32_3_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'a_unk_32_4', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'atlasinfo_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'name_foreach_textures', name_type_map['ArrayPointer'], (None, name_type_map['TextureData']), (False, None), (None, None)
		yield 'next_row_1', name_type_map['NextRow1'], (0, None), (False, None), (None, None)
		yield 'next_row_2', name_type_map['NextRow2'], (0, None), (False, None), (None, None)
		yield 'next_row_3', name_type_map['NextRow2'], (0, None), (False, None), (None, None)
		yield 'next_row_4', name_type_map['NextRow2'], (0, None), (False, None), (None, None)
		yield 'next_row_5', name_type_map['LastRow'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk_64_1', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_64_2', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_64_3', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_64_4', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_64_5', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_64_6', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_32_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_32_2_neg', name_type_map['Int'], (0, None), (False, None)
		yield 'unk_32_3', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_32_4', name_type_map['Uint'], (0, None), (False, None)
		yield 'a_unk_32_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'a_unk_32_2', name_type_map['Uint'], (0, None), (False, None)
		yield 'a_unk_32_3_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'a_unk_32_4', name_type_map['Uint'], (0, None), (False, None)
		yield 'atlasinfo_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'name_foreach_textures', name_type_map['ArrayPointer'], (instance.atlasinfo_count, name_type_map['TextureData']), (False, None)
		yield 'next_row_1', name_type_map['NextRow1'], (0, None), (False, None)
		yield 'next_row_2', name_type_map['NextRow2'], (0, None), (False, None)
		yield 'next_row_3', name_type_map['NextRow2'], (0, None), (False, None)
		yield 'next_row_4', name_type_map['NextRow2'], (0, None), (False, None)
		yield 'next_row_5', name_type_map['LastRow'], (0, None), (False, None)
