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

	_import_key = 'dinosaurmaterialvariants.compounds.DinoVariantsHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.has_sets = 0
		self.variant_count = 0
		self.zero = 0
		self.fgm_name = Pointer(self.context, 0, ZStringObfuscated)
		self.set_name = Pointer(self.context, 0, ZString)
		self.variants = Pointer(self.context, self.variant_count, DinoVariantsHeader._import_map["dinosaurmaterialvariants.compounds.VariantArray"])
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('fgm_name', Pointer, (0, ZStringObfuscated), (False, None), None),
		('has_sets', Uint64, (0, None), (False, None), None),
		('set_name', Pointer, (0, ZString), (False, None), None),
		('variants', Pointer, (None, None), (False, None), None),
		('variant_count', Uint64, (0, None), (False, None), None),
		('zero', Uint64, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'fgm_name', Pointer, (0, ZStringObfuscated), (False, None)
		yield 'has_sets', Uint64, (0, None), (False, None)
		yield 'set_name', Pointer, (0, ZString), (False, None)
		yield 'variants', Pointer, (instance.variant_count, DinoVariantsHeader._import_map["dinosaurmaterialvariants.compounds.VariantArray"]), (False, None)
		yield 'variant_count', Uint64, (0, None), (False, None)
		yield 'zero', Uint64, (0, None), (False, None)
