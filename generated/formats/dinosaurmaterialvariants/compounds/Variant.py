from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Variant(MemStruct):

	__name__ = 'Variant'

	_import_path = 'generated.formats.dinosaurmaterialvariants.compounds.Variant'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.has_ptr = 0
		self.variant_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.has_ptr = 0
		self.variant_name = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.has_ptr = Uint64.from_stream(stream, instance.context, 0, None)
		instance.variant_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		if not isinstance(instance.variant_name, int):
			instance.variant_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.has_ptr)
		Pointer.to_stream(stream, instance.variant_name)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'has_ptr', Uint64, (0, None), (False, None)
		yield 'variant_name', Pointer, (0, ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'Variant [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
