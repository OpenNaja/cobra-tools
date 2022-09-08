from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ChildSpecData(MemStruct):

	"""
	8 bytes
	eg. spineflex.specdef points to dependency for another specdef
	eg. flatridecontroller.specdef points to SpecdefRoot
	"""

	__name__ = 'ChildSpecData'

	_import_path = 'generated.formats.specdef.compounds.ChildSpecData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.specdef = Pointer(self.context, 0, ChildSpecData._import_path_map["generated.formats.specdef.compounds.SpecdefRoot"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.specdef = Pointer(self.context, 0, ChildSpecData._import_path_map["generated.formats.specdef.compounds.SpecdefRoot"])

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'specdef', Pointer, (0, ChildSpecData._import_path_map["generated.formats.specdef.compounds.SpecdefRoot"]), (False, None)

	def get_info_str(self, indent=0):
		return f'ChildSpecData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
