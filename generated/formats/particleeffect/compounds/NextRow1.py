from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class NextRow1(MemStruct):

	__name__ = 'nextRow1'

	_import_key = 'particleeffect.compounds.NextRow1'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk = 0
		self.garbage = 0
		self.value_1 = 0
		self.value_2 = 0
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('unk', Uint64, (0, None), (False, None), None),
		('garbage', Uint, (0, None), (False, None), None),
		('value_1', Ushort, (0, None), (False, None), None),
		('value_2', Ushort, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk', Uint64, (0, None), (False, None)
		yield 'garbage', Uint, (0, None), (False, None)
		yield 'value_1', Ushort, (0, None), (False, None)
		yield 'value_2', Ushort, (0, None), (False, None)
