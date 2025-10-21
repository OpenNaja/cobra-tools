from generated.formats.missiondata.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class MissionLevel(MemStruct):

	__name__ = 'MissionLevel'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.mission_level_path = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.mission_level_graph = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'mission_level_path', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'mission_level_graph', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'mission_level_path', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'mission_level_graph', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
