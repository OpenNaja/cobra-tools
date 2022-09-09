from generated.array import Array
from generated.formats.motiongraph.compounds.SinglePtr import SinglePtr
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class StateList(MemStruct):

	"""
	8 * arg bytes
	"""

	__name__ = 'StateList'

	_import_path = 'generated.formats.motiongraph.compounds.StateList'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ptrs = Array(self.context, 0, StateList._import_path_map["generated.formats.motiongraph.compounds.State"], (0,), SinglePtr)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ptrs', Array, (0, StateList._import_path_map["generated.formats.motiongraph.compounds.State"], (instance.arg,), SinglePtr), (False, None)

	def get_info_str(self, indent=0):
		return f'StateList [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
