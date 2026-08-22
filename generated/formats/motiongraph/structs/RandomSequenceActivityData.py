from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class RandomSequenceActivityData(MemStruct):

	__name__ = 'RandomSequenceActivityData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.num_activities = name_type_map['Uint64'](self.context, 0, None)
		self.unknown_0 = name_type_map['Uint'](self.context, 0, None)
		self.unknown_1 = name_type_map['Uint'](self.context, 0, None)
		self.unknown_2 = name_type_map['Uint'](self.context, 0, None)
		self.unknown_3 = name_type_map['Uint'](self.context, 0, None)
		self.unknown_4 = name_type_map['Uint'](self.context, 0, None)
		self.unknown_5 = name_type_map['Uint'](self.context, 0, None)
		self.unknown_6 = name_type_map['Ubyte'](self.context, 0, None)
		self.unknown_7 = name_type_map['Ubyte'](self.context, 0, None)
		self._padding_0 = name_type_map['Ushort'](self.context, 0, None)
		self.unknown_8 = name_type_map['Uint'](self.context, 0, None)
		self.unknown_9 = name_type_map['Uint64'](self.context, 0, None)
		self.initial_activity = name_type_map['Pointer'](self.context, 0, name_type_map['Activity'])
		self.activities = name_type_map['ArrayPointer'](self.context, self.num_activities, name_type_map['RandomSequenceActivityInfo'])
		self.variable = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'initial_activity', name_type_map['Pointer'], (0, name_type_map['Activity']), (False, None), (None, None)
		yield 'activities', name_type_map['ArrayPointer'], (None, name_type_map['RandomSequenceActivityInfo']), (False, None), (None, None)
		yield 'num_activities', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unknown_0', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_2', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_3', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_4', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_5', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_6', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'unknown_7', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield '_padding_0', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'unknown_8', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unknown_9', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'variable', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'initial_activity', name_type_map['Pointer'], (0, name_type_map['Activity']), (False, None)
		yield 'activities', name_type_map['ArrayPointer'], (instance.num_activities, name_type_map['RandomSequenceActivityInfo']), (False, None)
		yield 'num_activities', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unknown_0', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_2', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_3', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_4', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_5', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_6', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'unknown_7', name_type_map['Ubyte'], (0, None), (False, None)
		yield '_padding_0', name_type_map['Ushort'], (0, None), (False, None)
		yield 'unknown_8', name_type_map['Uint'], (0, None), (False, None)
		yield 'unknown_9', name_type_map['Uint64'], (0, None), (False, None)
		yield 'variable', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
