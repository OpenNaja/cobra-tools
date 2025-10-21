from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.semanticflexicolours.imports import name_type_map


class GameOverride(MemStruct):

	"""
	PZ: 32 bytes
	"""

	__name__ = 'GameOverride'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.game_names_count = name_type_map['Uint64'](self.context, 0, None)
		self.num_flexi_names = name_type_map['Uint64'](self.context, 0, None)
		self.game_names = name_type_map['Pointer'](self.context, self.game_names_count, name_type_map['ZStringList'])
		self.flexi_names = name_type_map['Pointer'](self.context, self.num_flexi_names, name_type_map['ZStringList'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'game_names', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'game_names_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'flexi_names', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'num_flexi_names', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'game_names', name_type_map['Pointer'], (instance.game_names_count, name_type_map['ZStringList']), (False, None)
		yield 'game_names_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'flexi_names', name_type_map['Pointer'], (instance.num_flexi_names, name_type_map['ZStringList']), (False, None)
		yield 'num_flexi_names', name_type_map['Uint64'], (0, None), (False, None)
