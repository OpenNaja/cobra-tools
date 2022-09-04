from generated.array import Array
from generated.formats.motiongraph.compounds.SinglePtr import SinglePtr
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class PtrList(MemStruct):

	"""
	8 * arg bytes
	"""

	__name__ = 'PtrList'

	_import_path = 'generated.formats.motiongraph.compounds.PtrList'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ptrs = Array(self.context, 0, self.template, (0,), SinglePtr)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.ptrs = Array(self.context, 0, self.template, (self.arg,), SinglePtr)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.ptrs = Array.from_stream(stream, instance.context, 0, instance.template, (instance.arg,), SinglePtr)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.ptrs, instance.context, 0, instance.template, (instance.arg,), SinglePtr)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'ptrs', Array, (0, instance.template, (instance.arg,), SinglePtr), (False, None)

	def get_info_str(self, indent=0):
		return f'PtrList [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
