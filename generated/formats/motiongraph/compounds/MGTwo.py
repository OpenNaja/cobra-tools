from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MGTwo(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'MGTwo'

	_import_path = 'generated.formats.motiongraph.compounds.MGTwo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.ptr = Pointer(self.context, self.count, MGTwo._import_path_map["generated.formats.motiongraph.compounds.PtrList"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count = 0
		self.ptr = Pointer(self.context, self.count, MGTwo._import_path_map["generated.formats.motiongraph.compounds.PtrList"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.ptr = Pointer.from_stream(stream, instance.context, instance.count, MGTwo._import_path_map["generated.formats.motiongraph.compounds.PtrList"])
		if not isinstance(instance.ptr, int):
			instance.ptr.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.count)
		Pointer.to_stream(stream, instance.ptr)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'count', Uint64, (0, None), (False, None)
		yield 'ptr', Pointer, (instance.count, MGTwo._import_path_map["generated.formats.motiongraph.compounds.PtrList"]), (False, None)

	def get_info_str(self, indent=0):
		return f'MGTwo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
