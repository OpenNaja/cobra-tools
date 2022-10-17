from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.basic import ZStringObfuscated
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class WeatherEventsRoot(MemStruct):

	__name__ = 'WeatherEventsRoot'

	_import_key = 'weatherevents.compounds.WeatherEventsRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.transition_time = 0.0
		self.unknown_1 = 0.0
		self.event_count = 0
		self.unknown_2 = 0
		self.resource_name = Pointer(self.context, 0, ZStringObfuscated)
		self.default_event_name = Pointer(self.context, 0, ZString)
		self.event_list = ArrayPointer(self.context, self.event_count, WeatherEventsRoot._import_map["weatherevents.compounds.WeatherEventData"])
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('resource_name', Pointer, (0, ZStringObfuscated), (False, None), None),
		('default_event_name', Pointer, (0, ZString), (False, None), None),
		('transition_time', Float, (0, None), (False, None), None),
		('unknown_1', Float, (0, None), (False, None), None),
		('event_list', ArrayPointer, (None, None), (False, None), None),
		('event_count', Uint64, (0, None), (False, None), None),
		('unknown_2', Uint64, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'resource_name', Pointer, (0, ZStringObfuscated), (False, None)
		yield 'default_event_name', Pointer, (0, ZString), (False, None)
		yield 'transition_time', Float, (0, None), (False, None)
		yield 'unknown_1', Float, (0, None), (False, None)
		yield 'event_list', ArrayPointer, (instance.event_count, WeatherEventsRoot._import_map["weatherevents.compounds.WeatherEventData"]), (False, None)
		yield 'event_count', Uint64, (0, None), (False, None)
		yield 'unknown_2', Uint64, (0, None), (False, None)
