from generated.array import Array
from generated.formats.motiongraph.compounds.ActivityEntry import ActivityEntry
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Activities(MemStruct):

	__name__ = 'Activities'

	_import_path = 'generated.formats.motiongraph.compounds.Activities'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.states = Array(self.context, 0, None, (0,), ActivityEntry)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.states = Array(self.context, 0, None, (self.arg,), ActivityEntry)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.states = Array.from_stream(stream, instance.context, 0, None, (instance.arg,), ActivityEntry)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.states, instance.context, 0, None, (instance.arg,), ActivityEntry)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'states', Array, (0, None, (instance.arg,), ActivityEntry), (False, None)

	def get_info_str(self, indent=0):
		return f'Activities [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
