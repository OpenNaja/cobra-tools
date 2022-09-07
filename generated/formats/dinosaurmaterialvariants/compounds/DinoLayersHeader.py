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
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.fgm_name = Pointer.from_stream(stream, instance.context, 0, ZStringObfuscated)
		instance.layers = ArrayPointer.from_stream(stream, instance.context, instance.layer_count, DinoLayersHeader._import_path_map["generated.formats.dinosaurmaterialvariants.compounds.Layer"])
		instance.layer_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.zero = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.fgm_name, int):
			instance.fgm_name.arg = 0
		if not isinstance(instance.layers, int):
			instance.layers.arg = instance.layer_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.fgm_name)
		ArrayPointer.to_stream(stream, instance.layers)
		Uint64.to_stream(stream, instance.layer_count)
		Uint64.to_stream(stream, instance.zero)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'fgm_name', Pointer, (0, ZStringObfuscated), (False, None)
		yield 'layers', ArrayPointer, (instance.layer_count, DinoLayersHeader._import_path_map["generated.formats.dinosaurmaterialvariants.compounds.Layer"]), (False, None)
		yield 'layer_count', Uint64, (0, None), (False, None)
		yield 'zero', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'DinoLayersHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
