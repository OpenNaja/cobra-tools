from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class LastRow(MemStruct):

	__name__ = 'LastRow'

	_import_key = 'particleeffect.compounds.LastRow'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_01 = 0
		self.unk_02 = 0
		self.unk_03 = 0
		self.unk_04 = 0
		self.unk_05 = 0
		self.unk_06 = 0
		self.unk_07 = 0
		self.unk_08 = 0
		self.unk_09 = 0
		self.unk_10 = 0
		self.unk_11 = 0
		self.unk_12 = 0
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('unk_01', Ushort, (0, None), (False, None), None),
		('unk_02', Ushort, (0, None), (False, None), None),
		('unk_03', Ushort, (0, None), (False, None), None),
		('unk_04', Ushort, (0, None), (False, None), None),
		('unk_05', Ushort, (0, None), (False, None), None),
		('unk_06', Ushort, (0, None), (False, None), None),
		('unk_07', Ushort, (0, None), (False, None), None),
		('unk_08', Ushort, (0, None), (False, None), None),
		('unk_09', Ushort, (0, None), (False, None), None),
		('unk_10', Ushort, (0, None), (False, None), None),
		('unk_11', Ushort, (0, None), (False, None), None),
		('unk_12', Ushort, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk_01', Ushort, (0, None), (False, None)
		yield 'unk_02', Ushort, (0, None), (False, None)
		yield 'unk_03', Ushort, (0, None), (False, None)
		yield 'unk_04', Ushort, (0, None), (False, None)
		yield 'unk_05', Ushort, (0, None), (False, None)
		yield 'unk_06', Ushort, (0, None), (False, None)
		yield 'unk_07', Ushort, (0, None), (False, None)
		yield 'unk_08', Ushort, (0, None), (False, None)
		yield 'unk_09', Ushort, (0, None), (False, None)
		yield 'unk_10', Ushort, (0, None), (False, None)
		yield 'unk_11', Ushort, (0, None), (False, None)
		yield 'unk_12', Ushort, (0, None), (False, None)
