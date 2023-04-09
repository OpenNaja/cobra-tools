from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class EventsList(MemStruct):

	__name__ = 'EventsList'

	_import_key = 'cinematic.compounds.EventsList'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.events = ArrayPointer(self.context, self.count, EventsList._import_map["cinematic.compounds.Event"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('events', ArrayPointer, (None, EventsList._import_map["cinematic.compounds.Event"]), (False, None), (None, None))
		yield ('count', Uint64, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'events', ArrayPointer, (instance.count, EventsList._import_map["cinematic.compounds.Event"]), (False, None)
		yield 'count', Uint64, (0, None), (False, None)
