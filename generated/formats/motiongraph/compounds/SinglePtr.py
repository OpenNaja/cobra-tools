from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class SinglePtr(MemStruct):

	"""
	8 bytes
	"""

	__name__ = 'SinglePtr'

	_import_path = 'generated.formats.motiongraph.compounds.SinglePtr'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ptr = Pointer(self.context, 0, self.template)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.ptr = Pointer(self.context, 0, self.template)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.ptr = Pointer.from_stream(stream, instance.context, 0, instance.template)
		if not isinstance(instance.ptr, int):
			instance.ptr.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.ptr)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'ptr', Pointer, (0, instance.template), (False, None)

	def get_info_str(self, indent=0):
		return f'SinglePtr [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
