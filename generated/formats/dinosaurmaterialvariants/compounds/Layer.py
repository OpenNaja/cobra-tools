from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Layer(MemStruct):

	__name__ = 'Layer'

	_import_path = 'generated.formats.dinosaurmaterialvariants.compounds.Layer'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.has_ptr = 0

		# defines the tiled texture material to be used
		self.texture_fgm_name = Pointer(self.context, 0, ZString)

		# defines how to transform the texture
		self.transform_fgm_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.has_ptr = 0
		self.texture_fgm_name = Pointer(self.context, 0, ZString)
		self.transform_fgm_name = Pointer(self.context, 0, ZString)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'has_ptr', Uint64, (0, None), (False, None)
		yield 'texture_fgm_name', Pointer, (0, ZString), (False, None)
		yield 'transform_fgm_name', Pointer, (0, ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'Layer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
