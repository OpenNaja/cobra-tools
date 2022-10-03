from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class UnlockState(MemStruct):

	__name__ = 'UnlockState'

	_import_key = 'animalresearch.compounds.UnlockState'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.entity_name = Pointer(self.context, 0, ZString)
		self.level_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('entity_name', Pointer, (0, ZString), (False, None), None),
		('level_name', Pointer, (0, ZString), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'entity_name', Pointer, (0, ZString), (False, None)
		yield 'level_name', Pointer, (0, ZString), (False, None)
