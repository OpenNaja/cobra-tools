from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class State(MemStruct):

	"""
	name uncertain
	40 bytes
	"""

	__name__ = 'State'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk = name_type_map['Uint'](self.context, 0, None)
		self.num_activities = name_type_map['Uint'](self.context, 0, None)
		self.array_2_count = name_type_map['Uint64'](self.context, 0, None)
		self.activities = name_type_map['ArrayPointer'](self.context, self.num_activities, name_type_map['ActivityReference'])
		self.array_2 = name_type_map['ArrayPointer'](self.context, self.array_2_count, name_type_map['TransStruct'])
		self.id = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'unk', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'num_activities', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'activities', name_type_map['ArrayPointer'], (None, name_type_map['ActivityReference']), (False, None), (None, None)
		yield 'array_2_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'array_2', name_type_map['ArrayPointer'], (None, name_type_map['TransStruct']), (False, None), (None, None)
		yield 'id', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk', name_type_map['Uint'], (0, None), (False, None)
		yield 'num_activities', name_type_map['Uint'], (0, None), (False, None)
		yield 'activities', name_type_map['ArrayPointer'], (instance.num_activities, name_type_map['ActivityReference']), (False, None)
		yield 'array_2_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'array_2', name_type_map['ArrayPointer'], (instance.array_2_count, name_type_map['TransStruct']), (False, None)
		yield 'id', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
