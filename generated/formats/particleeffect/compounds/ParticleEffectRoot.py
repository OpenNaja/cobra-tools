from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.particleeffect.compounds.LastRow import LastRow
from generated.formats.particleeffect.compounds.NextRow1 import NextRow1
from generated.formats.particleeffect.compounds.NextRow2 import NextRow2


class ParticleEffectRoot(MemStruct):

	__name__ = 'ParticleEffectRoot'

	_import_key = 'particleeffect.compounds.ParticleEffectRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_64_1 = 0
		self.unk_64_2 = 0
		self.unk_64_3 = 0
		self.unk_64_4 = 0
		self.unk_64_5 = 0
		self.unk_64_6 = 0
		self.unk_32_1 = 0
		self.unk_32_2_neg = 0
		self.unk_32_3 = 0
		self.unk_32_4 = 0
		self.a_unk_32_1 = 0
		self.a_unk_32_2 = 0
		self.a_unk_32_3_1 = 0
		self.a_unk_32_4 = 0
		self.atlasinfo_count = 0
		self.next_row_1 = NextRow1(self.context, 0, None)
		self.next_row_2 = NextRow2(self.context, 0, None)
		self.next_row_3 = NextRow2(self.context, 0, None)
		self.next_row_4 = NextRow2(self.context, 0, None)
		self.next_row_5 = LastRow(self.context, 0, None)
		self.name_foreach_textures = ArrayPointer(self.context, self.atlasinfo_count, ParticleEffectRoot._import_map["particleeffect.compounds.TextureData"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('unk_64_1', Uint64, (0, None), (False, None), (None, None))
		yield ('unk_64_2', Uint64, (0, None), (False, None), (None, None))
		yield ('unk_64_3', Uint64, (0, None), (False, None), (None, None))
		yield ('unk_64_4', Uint64, (0, None), (False, None), (None, None))
		yield ('unk_64_5', Uint64, (0, None), (False, None), (None, None))
		yield ('unk_64_6', Uint64, (0, None), (False, None), (None, None))
		yield ('unk_32_1', Uint, (0, None), (False, None), (None, None))
		yield ('unk_32_2_neg', Int, (0, None), (False, None), (None, None))
		yield ('unk_32_3', Uint, (0, None), (False, None), (None, None))
		yield ('unk_32_4', Uint, (0, None), (False, None), (None, None))
		yield ('a_unk_32_1', Uint, (0, None), (False, None), (None, None))
		yield ('a_unk_32_2', Uint, (0, None), (False, None), (None, None))
		yield ('a_unk_32_3_1', Uint, (0, None), (False, None), (None, None))
		yield ('a_unk_32_4', Uint, (0, None), (False, None), (None, None))
		yield ('atlasinfo_count', Uint64, (0, None), (False, None), (None, None))
		yield ('name_foreach_textures', ArrayPointer, (None, ParticleEffectRoot._import_map["particleeffect.compounds.TextureData"]), (False, None), (None, None))
		yield ('next_row_1', NextRow1, (0, None), (False, None), (None, None))
		yield ('next_row_2', NextRow2, (0, None), (False, None), (None, None))
		yield ('next_row_3', NextRow2, (0, None), (False, None), (None, None))
		yield ('next_row_4', NextRow2, (0, None), (False, None), (None, None))
		yield ('next_row_5', LastRow, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk_64_1', Uint64, (0, None), (False, None)
		yield 'unk_64_2', Uint64, (0, None), (False, None)
		yield 'unk_64_3', Uint64, (0, None), (False, None)
		yield 'unk_64_4', Uint64, (0, None), (False, None)
		yield 'unk_64_5', Uint64, (0, None), (False, None)
		yield 'unk_64_6', Uint64, (0, None), (False, None)
		yield 'unk_32_1', Uint, (0, None), (False, None)
		yield 'unk_32_2_neg', Int, (0, None), (False, None)
		yield 'unk_32_3', Uint, (0, None), (False, None)
		yield 'unk_32_4', Uint, (0, None), (False, None)
		yield 'a_unk_32_1', Uint, (0, None), (False, None)
		yield 'a_unk_32_2', Uint, (0, None), (False, None)
		yield 'a_unk_32_3_1', Uint, (0, None), (False, None)
		yield 'a_unk_32_4', Uint, (0, None), (False, None)
		yield 'atlasinfo_count', Uint64, (0, None), (False, None)
		yield 'name_foreach_textures', ArrayPointer, (instance.atlasinfo_count, ParticleEffectRoot._import_map["particleeffect.compounds.TextureData"]), (False, None)
		yield 'next_row_1', NextRow1, (0, None), (False, None)
		yield 'next_row_2', NextRow2, (0, None), (False, None)
		yield 'next_row_3', NextRow2, (0, None), (False, None)
		yield 'next_row_4', NextRow2, (0, None), (False, None)
		yield 'next_row_5', LastRow, (0, None), (False, None)
