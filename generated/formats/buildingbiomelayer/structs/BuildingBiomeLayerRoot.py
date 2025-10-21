from generated.formats.buildingbiomelayer.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class BuildingBiomeLayerRoot(MemStruct):

	__name__ = 'BuildingBiomeLayerRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = name_type_map['Uint64'](self.context, 0, None)
		self.unk_2_found_as_0 = name_type_map['Uint64'](self.context, 0, None)
		self.set_id_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZStringObfuscated'])
		self.layer_data = name_type_map['ArrayPointer'](self.context, self.count, name_type_map['BuildingBiomeData'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'set_id_name', name_type_map['Pointer'], (0, name_type_map['ZStringObfuscated']), (False, None), (None, None)
		yield 'layer_data', name_type_map['ArrayPointer'], (None, name_type_map['BuildingBiomeData']), (False, None), (None, None)
		yield 'count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk_2_found_as_0', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'set_id_name', name_type_map['Pointer'], (0, name_type_map['ZStringObfuscated']), (False, None)
		yield 'layer_data', name_type_map['ArrayPointer'], (instance.count, name_type_map['BuildingBiomeData']), (False, None)
		yield 'count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk_2_found_as_0', name_type_map['Uint64'], (0, None), (False, None)
