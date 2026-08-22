from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class TransitionConditionRecord(MemStruct):

	"""
	72-byte transition-local condition record.
	"""

	__name__ = 'TransitionConditionRecord'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.curve_length = name_type_map['Float'].from_value(-1.0)
		self.field_36 = name_type_map['Int'](self.context, 0, None)
		self.num_activities = name_type_map['Ushort'](self.context, 0, None)
		self.activity_flags = name_type_map['Ushort'](self.context, 0, None)
		self.field_44 = name_type_map['Uint'](self.context, 0, None)
		self.decision_instructions = name_type_map['AllocationArrayPointer'](self.context, 0, name_type_map['MRFMember1'])
		self.field_56 = name_type_map['Short'](self.context, 0, None)
		self.tier = name_type_map['Ushort'](self.context, 0, None)
		self.field_60 = name_type_map['Int'](self.context, 0, None)
		self.transition = name_type_map['Pointer'](self.context, 0, name_type_map['Transition'])
		self.curve = name_type_map['Pointer'](self.context, 0, None)
		self.trigger = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.activities = name_type_map['ArrayPointer'](self.context, self.num_activities, name_type_map['ActivityReference'])
		self.id = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'transition', name_type_map['Pointer'], (0, name_type_map['Transition']), (False, None), (None, None)
		yield 'curve', name_type_map['Pointer'], (0, None), (False, None), (None, None)
		yield 'trigger', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'activities', name_type_map['ArrayPointer'], (None, name_type_map['ActivityReference']), (False, None), (None, None)
		yield 'curve_length', name_type_map['Float'], (0, None), (False, -1.0), (None, None)
		yield 'field_36', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'num_activities', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'activity_flags', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'field_44', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'decision_instructions', name_type_map['AllocationArrayPointer'], (0, name_type_map['MRFMember1']), (False, None), (None, None)
		yield 'field_56', name_type_map['Short'], (0, None), (False, None), (None, None)
		yield 'tier', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'field_60', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'id', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'transition', name_type_map['Pointer'], (0, name_type_map['Transition']), (False, None)
		yield 'curve', name_type_map['Pointer'], (0, None), (False, None)
		yield 'trigger', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'activities', name_type_map['ArrayPointer'], (instance.num_activities, name_type_map['ActivityReference']), (False, None)
		yield 'curve_length', name_type_map['Float'], (0, None), (False, -1.0)
		yield 'field_36', name_type_map['Int'], (0, None), (False, None)
		yield 'num_activities', name_type_map['Ushort'], (0, None), (False, None)
		yield 'activity_flags', name_type_map['Ushort'], (0, None), (False, None)
		yield 'field_44', name_type_map['Uint'], (0, None), (False, None)
		yield 'decision_instructions', name_type_map['AllocationArrayPointer'], (0, name_type_map['MRFMember1']), (False, None)
		yield 'field_56', name_type_map['Short'], (0, None), (False, None)
		yield 'tier', name_type_map['Ushort'], (0, None), (False, None)
		yield 'field_60', name_type_map['Int'], (0, None), (False, None)
		yield 'id', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)

	def get_ptr_template(self, prop):
		if prop == "curve":
			return name_type_map["CurveData"]

