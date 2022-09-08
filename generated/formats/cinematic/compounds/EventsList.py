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
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'events', ArrayPointer, (instance.count, EventsList._import_path_map["generated.formats.cinematic.compounds.Event"]), (False, None)
		yield 'count', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'EventsList [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
