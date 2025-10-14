from generated.formats.cinematic.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class EventsList(MemStruct):

	__name__ = 'EventsList'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.num_events = name_type_map['Uint64'](self.context, 0, None)
		self.events = name_type_map['ArrayPointer'](self.context, self.num_events, name_type_map['Event'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'events', name_type_map['ArrayPointer'], (None, name_type_map['Event']), (False, None), (None, None)
		yield 'num_events', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'events', name_type_map['ArrayPointer'], (instance.num_events, name_type_map['Event']), (False, None)
		yield 'num_events', name_type_map['Uint64'], (0, None), (False, None)
