from generated.formats.navigationsettings.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class NavigationAreaCostsFilter(MemStruct):

	__name__ = 'NavigationAreaCostsFilter'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.navigation_area_costs_count = name_type_map['Uint64'](self.context, 0, None)
		self.navigation_area_costs_filter_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.navigation_area_costs = name_type_map['ArrayPointer'](self.context, self.navigation_area_costs_count, name_type_map['NavigationAreaCostsData'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'navigation_area_costs_filter_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'navigation_area_costs', name_type_map['ArrayPointer'], (None, name_type_map['NavigationAreaCostsData']), (False, None), (None, None)
		yield 'navigation_area_costs_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'navigation_area_costs_filter_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'navigation_area_costs', name_type_map['ArrayPointer'], (instance.navigation_area_costs_count, name_type_map['NavigationAreaCostsData']), (False, None)
		yield 'navigation_area_costs_count', name_type_map['Uint64'], (0, None), (False, None)
