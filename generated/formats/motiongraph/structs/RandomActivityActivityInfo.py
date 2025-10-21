from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class RandomActivityActivityInfo(MemStruct):

	__name__ = 'RandomActivityActivityInfo'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.weighting = name_type_map['Uint'](self.context, 0, None)
		self._padding = name_type_map['Uint'](self.context, 0, None)
		self.activity = name_type_map['Pointer'](self.context, 0, name_type_map['Activity'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'activity', name_type_map['Pointer'], (0, name_type_map['Activity']), (False, None), (None, None)
		yield 'weighting', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield '_padding', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'activity', name_type_map['Pointer'], (0, name_type_map['Activity']), (False, None)
		yield 'weighting', name_type_map['Uint'], (0, None), (False, None)
		yield '_padding', name_type_map['Uint'], (0, None), (False, None)
