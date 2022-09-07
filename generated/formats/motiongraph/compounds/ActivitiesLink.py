from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ActivitiesLink(MemStruct):

	__name__ = 'ActivitiesLink'

	_import_path = 'generated.formats.motiongraph.compounds.ActivitiesLink'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.linked = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.linked = Pointer(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.linked = Pointer.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.linked, int):
			instance.linked.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.linked)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'linked', Pointer, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'ActivitiesLink [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
