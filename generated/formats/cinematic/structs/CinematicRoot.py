from generated.formats.cinematic.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class CinematicRoot(MemStruct):

	__name__ = 'CinematicRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.names_count = name_type_map['Uint64'](self.context, 0, None)
		self.data_count = name_type_map['Uint64'](self.context, 0, None)
		self.names = name_type_map['Pointer'](self.context, self.names_count, name_type_map['ZStringList'])
		self.data = name_type_map['ArrayPointer'](self.context, self.data_count, name_type_map['CinematicData'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'names', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'names_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'data', name_type_map['ArrayPointer'], (None, name_type_map['CinematicData']), (False, None), (None, None)
		yield 'data_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'names', name_type_map['Pointer'], (instance.names_count, name_type_map['ZStringList']), (False, None)
		yield 'names_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'data', name_type_map['ArrayPointer'], (instance.data_count, name_type_map['CinematicData']), (False, None)
		yield 'data_count', name_type_map['Uint64'], (0, None), (False, None)
