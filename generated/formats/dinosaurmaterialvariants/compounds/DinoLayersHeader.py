from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.basic import ZStringObfuscated
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class DinoLayersHeader(MemStruct):

	__name__ = 'DinoLayersHeader'

	_import_path = 'generated.formats.dinosaurmaterialvariants.compounds.DinoLayersHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.layer_count = 0
		self.zero = 0
		self.fgm_name = Pointer(self.context, 0, ZStringObfuscated)
		self.layers = ArrayPointer(self.context, self.layer_count, DinoLayersHeader._import_path_map["generated.formats.dinosaurmaterialvariants.compounds.Layer"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.layer_count = 0
		self.zero = 0
		self.fgm_name = Pointer(self.context, 0, ZStringObfuscated)
		self.layers = ArrayPointer(self.context, self.layer_count, DinoLayersHeader._import_path_map["generated.formats.dinosaurmaterialvariants.compounds.Layer"])

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'fgm_name', Pointer, (0, ZStringObfuscated), (False, None)
		yield 'layers', ArrayPointer, (instance.layer_count, DinoLayersHeader._import_path_map["generated.formats.dinosaurmaterialvariants.compounds.Layer"]), (False, None)
		yield 'layer_count', Uint64, (0, None), (False, None)
		yield 'zero', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'DinoLayersHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
