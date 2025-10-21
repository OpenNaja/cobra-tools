from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class MRFMember2(MemStruct):

	"""
	72 bytes
	only used if transition is in 'id'
	"""

	__name__ = 'MRFMember2'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count_0 = name_type_map['Uint64'](self.context, 0, None)
		self.count_3_a = name_type_map['Short'](self.context, 0, None)
		self.count_3_b = name_type_map['Short'](self.context, 0, None)
		self.count_3_c = name_type_map['Int'](self.context, 0, None)
		self.num_activities = name_type_map['Uint64'](self.context, 0, None)
		self.count_5 = name_type_map['Uint64'](self.context, 0, None)
		self.count_6_a = name_type_map['Short'](self.context, 0, None)
		self.count_6_b = name_type_map['Short'](self.context, 0, None)
		self.count_6_c = name_type_map['Int'](self.context, 0, None)
		self.transition = name_type_map['Pointer'](self.context, 0, name_type_map['Transition'])
		self.trigger = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.activities = name_type_map['Pointer'](self.context, self.num_activities, name_type_map['ActivityReference'])
		self.id = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'transition', name_type_map['Pointer'], (0, name_type_map['Transition']), (False, None), (None, None)
		yield 'count_0', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'trigger', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'activities', name_type_map['Pointer'], (None, name_type_map['ActivityReference']), (False, None), (None, None)
		yield 'count_3_a', name_type_map['Short'], (0, None), (False, None), (None, None)
		yield 'count_3_b', name_type_map['Short'], (0, None), (False, None), (None, None)
		yield 'count_3_c', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'num_activities', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'count_5', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'count_6_a', name_type_map['Short'], (0, None), (False, None), (None, None)
		yield 'count_6_b', name_type_map['Short'], (0, None), (False, None), (None, None)
		yield 'count_6_c', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'id', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'transition', name_type_map['Pointer'], (0, name_type_map['Transition']), (False, None)
		yield 'count_0', name_type_map['Uint64'], (0, None), (False, None)
		yield 'trigger', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'activities', name_type_map['Pointer'], (instance.num_activities, name_type_map['ActivityReference']), (False, None)
		yield 'count_3_a', name_type_map['Short'], (0, None), (False, None)
		yield 'count_3_b', name_type_map['Short'], (0, None), (False, None)
		yield 'count_3_c', name_type_map['Int'], (0, None), (False, None)
		yield 'num_activities', name_type_map['Uint64'], (0, None), (False, None)
		yield 'count_5', name_type_map['Uint64'], (0, None), (False, None)
		yield 'count_6_a', name_type_map['Short'], (0, None), (False, None)
		yield 'count_6_b', name_type_map['Short'], (0, None), (False, None)
		yield 'count_6_c', name_type_map['Int'], (0, None), (False, None)
		yield 'id', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
