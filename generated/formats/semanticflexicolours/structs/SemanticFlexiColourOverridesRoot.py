from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.semanticflexicolours.imports import name_type_map


class SemanticFlexiColourOverridesRoot(MemStruct):

	__name__ = 'SemanticFlexiColourOverridesRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.num_color_overrides = name_type_map['Ushort'](self.context, 0, None)
		self.num_game_overrides = name_type_map['Ushort'](self.context, 0, None)
		self._z_0 = name_type_map['Int'](self.context, 0, None)
		self._z_1 = name_type_map['Uint64'](self.context, 0, None)
		self.color_overrides = name_type_map['ArrayPointer'](self.context, self.num_color_overrides, name_type_map['ColorOverride'])
		self.game_overrides = name_type_map['ArrayPointer'](self.context, self.num_game_overrides, name_type_map['GameOverride'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'color_overrides', name_type_map['ArrayPointer'], (None, name_type_map['ColorOverride']), (False, None), (None, None)
		yield 'game_overrides', name_type_map['ArrayPointer'], (None, name_type_map['GameOverride']), (False, None), (None, None)
		yield 'num_color_overrides', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'num_game_overrides', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield '_z_0', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield '_z_1', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'color_overrides', name_type_map['ArrayPointer'], (instance.num_color_overrides, name_type_map['ColorOverride']), (False, None)
		yield 'game_overrides', name_type_map['ArrayPointer'], (instance.num_game_overrides, name_type_map['GameOverride']), (False, None)
		yield 'num_color_overrides', name_type_map['Ushort'], (0, None), (False, None)
		yield 'num_game_overrides', name_type_map['Ushort'], (0, None), (False, None)
		yield '_z_0', name_type_map['Int'], (0, None), (False, None)
		yield '_z_1', name_type_map['Uint64'], (0, None), (False, None)
