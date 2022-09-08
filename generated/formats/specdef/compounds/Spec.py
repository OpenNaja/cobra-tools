from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.specdef.enums.SpecdefDtype import SpecdefDtype


class Spec(MemStruct):

	__name__ = 'Spec'

	_import_path = 'generated.formats.specdef.compounds.Spec'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.dtype = SpecdefDtype(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'dtype', SpecdefDtype, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Spec [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
