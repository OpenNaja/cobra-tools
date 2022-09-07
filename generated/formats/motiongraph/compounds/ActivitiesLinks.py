from generated.array import Array
from generated.formats.motiongraph.compounds.ActivitiesLink import ActivitiesLink
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class ActivitiesLinks(MemStruct):

	__name__ = 'ActivitiesLinks'

	_import_path = 'generated.formats.motiongraph.compounds.ActivitiesLinks'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.activities = Array(self.context, 0, None, (0,), ActivitiesLink)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.activities = Array(self.context, 0, None, (self.arg,), ActivitiesLink)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.activities = Array.from_stream(stream, instance.context, 0, None, (instance.arg,), ActivitiesLink)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.activities, ActivitiesLink)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'activities', Array, (0, None, (instance.arg,), ActivitiesLink), (False, None)

	def get_info_str(self, indent=0):
		return f'ActivitiesLinks [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
