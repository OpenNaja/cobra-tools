from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Variant(MemStruct):

	__name__ = 'Variant'

	_import_key = 'dinosaurmaterialvariants.compounds.Variant'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.has_ptr = 0
		self.variant_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('has_ptr', Uint64, (0, None), (False, None), (None, None))
		yield ('variant_name', Pointer, (0, ZString), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'has_ptr', Uint64, (0, None), (False, None)
		yield 'variant_name', Pointer, (0, ZString), (False, None)


Variant.init_attributes()
