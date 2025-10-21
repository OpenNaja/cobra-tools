from generated.formats.missiondata.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class MissionLevelDifficultyList(MemStruct):

	__name__ = 'MissionLevelDifficultyList'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.mission_level_difficulty_list = name_type_map['Pointer'](self.context, 0, name_type_map['MissionLevelDifficulty'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'mission_level_difficulty_list', name_type_map['Pointer'], (0, name_type_map['MissionLevelDifficulty']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'mission_level_difficulty_list', name_type_map['Pointer'], (0, name_type_map['MissionLevelDifficulty']), (False, None)
