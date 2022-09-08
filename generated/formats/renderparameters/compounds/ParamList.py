from generated.array import Array
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ParamList(MemStruct):

	"""
	this is not null ptr terminated, but padded to 16 bytes at the end
	"""

	__name__ = 'ParamList'

	_import_path = 'generated.formats.renderparameters.compounds.ParamList'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ptrs = Array(self.context, 0, ParamList._import_path_map["generated.formats.renderparameters.compounds.Param"], (0,), Pointer)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.ptrs = Array(self.context, 0, ParamList._import_path_map["generated.formats.renderparameters.compounds.Param"], (self.arg,), Pointer)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ptrs', Array, (0, ParamList._import_path_map["generated.formats.renderparameters.compounds.Param"], (instance.arg,), Pointer), (False, None)

	def get_info_str(self, indent=0):
		return f'ParamList [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
