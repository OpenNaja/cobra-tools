from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.specdef.enums.SpecdefDtype import SpecdefDtype


class ArrayData(MemStruct):

	"""
	16 bytes in log
	"""

	__name__ = 'ArrayData'

	_import_key = 'specdef.compounds.ArrayData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.dtype = SpecdefDtype(self.context, 0, None)
		self.unused = 0
		self.item = Pointer(self.context, self.dtype, ArrayData._import_map["specdef.compounds.Data"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('item', Pointer, (None, ArrayData._import_map["specdef.compounds.Data"]), (False, None), (None, None))
		yield ('dtype', SpecdefDtype, (0, None), (False, None), (None, None))
		yield ('unused', Uint, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'item', Pointer, (instance.dtype, ArrayData._import_map["specdef.compounds.Data"]), (False, None)
		yield 'dtype', SpecdefDtype, (0, None), (False, None)
		yield 'unused', Uint, (0, None), (False, None)


ArrayData.init_attributes()
