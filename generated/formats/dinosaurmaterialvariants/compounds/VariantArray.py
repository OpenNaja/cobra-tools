from generated.array import Array
from generated.formats.dinosaurmaterialvariants.compounds.Variant import Variant
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class VariantArray(MemStruct):

	__name__ = 'VariantArray'

	_import_path = 'generated.formats.dinosaurmaterialvariants.compounds.VariantArray'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.variants = Array(self.context, 0, None, (0,), Variant)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.variants = Array(self.context, 0, None, (self.arg,), Variant)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.variants = Array.from_stream(stream, instance.context, 0, None, (instance.arg,), Variant)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.variants, Variant)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'variants', Array, (0, None, (instance.arg,), Variant), (False, None)

	def get_info_str(self, indent=0):
		return f'VariantArray [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
