from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class RandomActivityActivityInfoData(MemStruct):

	"""
	bytes
	"""

	__name__ = 'RandomActivityActivityInfoData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.num_activities = name_type_map['Uint'](self.context, 0, None)
		self.blend_time = name_type_map['Float'](self.context, 0, None)
		self.mode = name_type_map['SelectActivityActivityMode'](self.context, 0, None)
		self.enum_variable = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.activities = name_type_map['ArrayPointer'](self.context, self.num_activities, name_type_map['ActivityReference'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'enum_variable', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'activities', name_type_map['ArrayPointer'], (None, name_type_map['ActivityReference']), (False, None), (None, None)
		yield 'num_activities', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'blend_time', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'mode', name_type_map['SelectActivityActivityMode'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'enum_variable', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'activities', name_type_map['ArrayPointer'], (instance.num_activities, name_type_map['ActivityReference']), (False, None)
		yield 'num_activities', name_type_map['Uint'], (0, None), (False, None)
		yield 'blend_time', name_type_map['Float'], (0, None), (False, None)
		yield 'mode', name_type_map['SelectActivityActivityMode'], (0, None), (False, None)
