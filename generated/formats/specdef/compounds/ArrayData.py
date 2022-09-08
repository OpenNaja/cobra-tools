from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.specdef.enums.SpecdefDtype import SpecdefDtype


class ArrayData(MemStruct):

	"""
	16 bytes in log
	"""

	__name__ = 'ArrayData'

	_import_path = 'generated.formats.specdef.compounds.ArrayData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.dtype = SpecdefDtype(self.context, 0, None)
		self.unused = 0
		self.item = Pointer(self.context, self.dtype, ArrayData._import_path_map["generated.formats.specdef.compounds.Data"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		# leaving self.dtype alone
		self.unused = 0
		self.item = Pointer(self.context, self.dtype, ArrayData._import_path_map["generated.formats.specdef.compounds.Data"])

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'item', Pointer, (instance.dtype, ArrayData._import_path_map["generated.formats.specdef.compounds.Data"]), (False, None)
		yield 'dtype', SpecdefDtype, (0, None), (False, None)
		yield 'unused', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'ArrayData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
