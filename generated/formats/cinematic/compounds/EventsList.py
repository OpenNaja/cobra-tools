from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class EventsList(MemStruct):

	__name__ = 'EventsList'

	_import_path = 'generated.formats.cinematic.compounds.EventsList'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.events = ArrayPointer(self.context, self.count, EventsList._import_path_map["generated.formats.cinematic.compounds.Event"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count = 0
		self.events = ArrayPointer(self.context, self.count, EventsList._import_path_map["generated.formats.cinematic.compounds.Event"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.events = ArrayPointer.from_stream(stream, instance.context, instance.count, EventsList._import_path_map["generated.formats.cinematic.compounds.Event"])
		instance.count = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.events, int):
			instance.events.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		ArrayPointer.to_stream(stream, instance.events)
		Uint64.to_stream(stream, instance.count)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'events', ArrayPointer, (instance.count, EventsList._import_path_map["generated.formats.cinematic.compounds.Event"]), (False, None)
		yield 'count', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'EventsList [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
