from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.researchdata.imports import name_type_map


class SubResearchFXData(MemStruct):

	__name__ = 'SubResearchFXData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.fx_name = name_type_map['Pointer'](self.context, 0, name_type_map['FxDataName'])
		self.fx_params = name_type_map['Pointer'](self.context, 0, name_type_map['FxDataSettings'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'fx_name', name_type_map['Pointer'], (0, name_type_map['FxDataName']), (False, None), (None, None)
		yield 'fx_params', name_type_map['Pointer'], (0, name_type_map['FxDataSettings']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'fx_name', name_type_map['Pointer'], (0, name_type_map['FxDataName']), (False, None)
		yield 'fx_params', name_type_map['Pointer'], (0, name_type_map['FxDataSettings']), (False, None)
