from generated.formats.base.basic import fmt_member
import generated.formats.dinosaurmaterialvariants.compound.Layer
import generated.formats.ovl_base.basic
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class DinoLayersHeader(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)
		self.layer_count = 0
		self.zero = 0
		self.fgm_name = 0
		self.layers = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.layer_count = 0
		self.zero = 0
		self.fgm_name = Pointer(self.context, 0, generated.formats.ovl_base.basic.ZStringObfuscated)
		self.layers = ArrayPointer(self.context, self.layer_count, generated.formats.dinosaurmaterialvariants.compound.Layer.Layer)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.fgm_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.ovl_base.basic.ZStringObfuscated)
		instance.layers = ArrayPointer.from_stream(stream, instance.context, instance.layer_count, generated.formats.dinosaurmaterialvariants.compound.Layer.Layer)
		instance.layer_count = stream.read_uint64()
		instance.zero = stream.read_uint64()
		instance.fgm_name.arg = 0
		instance.layers.arg = instance.layer_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.fgm_name)
		ArrayPointer.to_stream(stream, instance.layers)
		stream.write_uint64(instance.layer_count)
		stream.write_uint64(instance.zero)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('fgm_name', Pointer, (0, generated.formats.ovl_base.basic.ZStringObfuscated))
		yield ('layers', ArrayPointer, (instance.layer_count, generated.formats.dinosaurmaterialvariants.compound.Layer.Layer))
		yield ('layer_count', Uint64, (0, None))
		yield ('zero', Uint64, (0, None))

	def get_info_str(self, indent=0):
		return f'DinoLayersHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* fgm_name = {fmt_member(self.fgm_name, indent+1)}'
		s += f'\n	* layers = {fmt_member(self.layers, indent+1)}'
		s += f'\n	* layer_count = {fmt_member(self.layer_count, indent+1)}'
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
