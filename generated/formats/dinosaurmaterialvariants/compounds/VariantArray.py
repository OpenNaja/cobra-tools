from generated.array import Array
from generated.formats.dinosaurmaterialvariants.compounds.Variant import Variant
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class VariantArray(MemStruct):

	__name__ = 'VariantArray'

	_import_key = 'dinosaurmaterialvariants.compounds.VariantArray'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.variants = Array(self.context, 0, None, (0,), Variant)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'variants', Array, (0, None, (instance.arg,), Variant), (False, None)
