from generated.formats.animalresearch.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class ResearchStartRoot(MemStruct):

	__name__ = 'ResearchStartRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.states_count = name_type_map['Uint64'](self.context, 0, None)
		self.states = name_type_map['ArrayPointer'](self.context, self.states_count, name_type_map['UnlockState'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'states', name_type_map['ArrayPointer'], (None, name_type_map['UnlockState']), (False, None), (None, None)
		yield 'states_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'states', name_type_map['ArrayPointer'], (instance.states_count, name_type_map['UnlockState']), (False, None)
		yield 'states_count', name_type_map['Uint64'], (0, None), (False, None)
