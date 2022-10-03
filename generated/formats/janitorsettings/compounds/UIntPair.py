from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class UIntPair(MemStruct):

	__name__ = 'UIntPair'

	_import_key = 'janitorsettings.compounds.UIntPair'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.value_0 = 0
		self.value_1 = 0
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('value_0', Uint, (0, None), (False, None), None),
		('value_1', Uint, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'value_0', Uint, (0, None), (False, None)
		yield 'value_1', Uint, (0, None), (False, None)
