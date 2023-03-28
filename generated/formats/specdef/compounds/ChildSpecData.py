from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ChildSpecData(MemStruct):

	"""
	8 bytes
	eg. spineflex.specdef points to dependency for another specdef
	eg. flatridecontroller.specdef points to SpecdefRoot
	"""

	__name__ = 'ChildSpecData'

	_import_key = 'specdef.compounds.ChildSpecData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.specdef = Pointer(self.context, 0, ChildSpecData._import_map["specdef.compounds.SpecdefRoot"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('specdef', Pointer, (0, ChildSpecData._import_map["specdef.compounds.SpecdefRoot"]), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'specdef', Pointer, (0, ChildSpecData._import_map["specdef.compounds.SpecdefRoot"]), (False, None)


ChildSpecData.init_attributes()
