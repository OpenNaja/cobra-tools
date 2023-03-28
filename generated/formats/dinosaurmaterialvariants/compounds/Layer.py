from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Layer(MemStruct):

	__name__ = 'Layer'

	_import_key = 'dinosaurmaterialvariants.compounds.Layer'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.has_ptr = 0

		# defines the tiled texture material to be used
		self.texture_fgm_name = Pointer(self.context, 0, ZString)

		# defines how to transform the texture
		self.transform_fgm_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('has_ptr', Uint64, (0, None), (False, None), (None, None))
		yield ('texture_fgm_name', Pointer, (0, ZString), (False, None), (None, None))
		yield ('transform_fgm_name', Pointer, (0, ZString), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'has_ptr', Uint64, (0, None), (False, None)
		yield 'texture_fgm_name', Pointer, (0, ZString), (False, None)
		yield 'transform_fgm_name', Pointer, (0, ZString), (False, None)


Layer.init_attributes()
