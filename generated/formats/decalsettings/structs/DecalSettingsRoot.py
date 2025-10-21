from generated.formats.decalsettings.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class DecalSettingsRoot(MemStruct):

	__name__ = 'DecalSettingsRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.layer_count = name_type_map['Uint64'](self.context, 0, None)
		self.unknown = name_type_map['Uint64'](self.context, 0, None)
		self.atlas_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.layer_list = name_type_map['ArrayPointer'](self.context, self.layer_count, name_type_map['DecalSettingItem'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'atlas_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'layer_list', name_type_map['ArrayPointer'], (None, name_type_map['DecalSettingItem']), (False, None), (None, None)
		yield 'layer_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unknown', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'atlas_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'layer_list', name_type_map['ArrayPointer'], (instance.layer_count, name_type_map['DecalSettingItem']), (False, None)
		yield 'layer_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unknown', name_type_map['Uint64'], (0, None), (False, None)
