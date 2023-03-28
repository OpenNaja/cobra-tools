from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class PoseDriverDefRoot(MemStruct):

	__name__ = 'PoseDriverDefRoot'

	_import_key = 'posedriverdef.compounds.PoseDriverDefRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.drivers = ArrayPointer(self.context, self.count, PoseDriverDefRoot._import_map["posedriverdef.compounds.Driver"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('drivers', ArrayPointer, (None, PoseDriverDefRoot._import_map["posedriverdef.compounds.Driver"]), (False, None), None)
		yield ('count', Uint64, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'drivers', ArrayPointer, (instance.count, PoseDriverDefRoot._import_map["posedriverdef.compounds.Driver"]), (False, None)
		yield 'count', Uint64, (0, None), (False, None)


PoseDriverDefRoot.init_attributes()
