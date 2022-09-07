from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.basic import ZStringObfuscated
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class DinoVariantsHeader(MemStruct):

	"""
	# set_count - seen either 0 or 1, could possibly be more, would need refactor in that case
	# no set_count for rex 93 - has no materialpatterns, so that's probably why it's different
	"""

	__name__ = 'DinoVariantsHeader'

	_import_path = 'generated.formats.dinosaurmaterialvariants.compounds.DinoVariantsHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.has_sets = 0
		self.variant_count = 0
		self.zero = 0
		self.fgm_name = Pointer(self.context, 0, ZStringObfuscated)
		self.set_name = Pointer(self.context, 0, ZString)
		self.variants = Pointer(self.context, self.variant_count, DinoVariantsHeader._import_path_map["generated.formats.dinosaurmaterialvariants.compounds.VariantArray"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.has_sets = 0
		self.variant_count = 0
		self.zero = 0
		self.fgm_name = Pointer(self.context, 0, ZStringObfuscated)
		self.set_name = Pointer(self.context, 0, ZString)
		self.variants = Pointer(self.context, self.variant_count, DinoVariantsHeader._import_path_map["generated.formats.dinosaurmaterialvariants.compounds.VariantArray"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.fgm_name = Pointer.from_stream(stream, instance.context, 0, ZStringObfuscated)
		instance.has_sets = Uint64.from_stream(stream, instance.context, 0, None)
		instance.set_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.variants = Pointer.from_stream(stream, instance.context, instance.variant_count, DinoVariantsHeader._import_path_map["generated.formats.dinosaurmaterialvariants.compounds.VariantArray"])
		instance.variant_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.zero = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.fgm_name, int):
			instance.fgm_name.arg = 0
		if not isinstance(instance.set_name, int):
			instance.set_name.arg = 0
		if not isinstance(instance.variants, int):
			instance.variants.arg = instance.variant_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.fgm_name)
		Uint64.to_stream(stream, instance.has_sets)
		Pointer.to_stream(stream, instance.set_name)
		Pointer.to_stream(stream, instance.variants)
		Uint64.to_stream(stream, instance.variant_count)
		Uint64.to_stream(stream, instance.zero)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'fgm_name', Pointer, (0, ZStringObfuscated), (False, None)
		yield 'has_sets', Uint64, (0, None), (False, None)
		yield 'set_name', Pointer, (0, ZString), (False, None)
		yield 'variants', Pointer, (instance.variant_count, DinoVariantsHeader._import_path_map["generated.formats.dinosaurmaterialvariants.compounds.VariantArray"]), (False, None)
		yield 'variant_count', Uint64, (0, None), (False, None)
		yield 'zero', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'DinoVariantsHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
