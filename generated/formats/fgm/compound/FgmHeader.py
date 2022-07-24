from source.formats.base.basic import fmt_member
import generated.formats.fgm.compound.AttribData
import generated.formats.fgm.compound.AttributeInfo
import generated.formats.fgm.compound.DependencyInfo
import generated.formats.fgm.compound.TextureInfo
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.ForEachPointer import ForEachPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class FgmHeader(MemStruct):

	"""
	# JWE2 patternset fgms seem to be in pool type 3, everything else in 2
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.texture_count = 0
		self.texture_count = 0
		self.attribute_count = 0
		self.attribute_count = 0
		self.unk_0 = 0
		self.unk_1 = 0
		self.textures = 0
		self.attributes = 0
		self.dependencies = 0
		self.data_lib = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if self.context.version <= 15:
			self.texture_count = 0
		if self.context.version >= 17:
			self.texture_count = 0
		if self.context.version <= 15:
			self.attribute_count = 0
		if self.context.version >= 17:
			self.attribute_count = 0
		self.unk_0 = 0
		self.unk_1 = 0
		self.textures = ArrayPointer(self.context, self.texture_count, generated.formats.fgm.compound.TextureInfo.TextureInfo)
		self.attributes = ArrayPointer(self.context, self.attribute_count, generated.formats.fgm.compound.AttributeInfo.AttributeInfo)
		self.dependencies = ForEachPointer(self.context, self.textures, generated.formats.fgm.compound.DependencyInfo.DependencyInfo)
		self.data_lib = ForEachPointer(self.context, self.attributes, generated.formats.fgm.compound.AttribData.AttribData)

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
		if instance.context.version <= 15:
			instance.texture_count = stream.read_uint()
		if instance.context.version >= 17:
			instance.texture_count = stream.read_uint64()
		if instance.context.version <= 15:
			instance.attribute_count = stream.read_uint()
		if instance.context.version >= 17:
			instance.attribute_count = stream.read_uint64()
		instance.textures = ArrayPointer.from_stream(stream, instance.context, instance.texture_count, generated.formats.fgm.compound.TextureInfo.TextureInfo)
		instance.attributes = ArrayPointer.from_stream(stream, instance.context, instance.attribute_count, generated.formats.fgm.compound.AttributeInfo.AttributeInfo)
		instance.dependencies = ForEachPointer.from_stream(stream, instance.context, instance.textures, generated.formats.fgm.compound.DependencyInfo.DependencyInfo)
		instance.data_lib = ForEachPointer.from_stream(stream, instance.context, instance.attributes, generated.formats.fgm.compound.AttribData.AttribData)
		instance.unk_0 = stream.read_uint64()
		instance.unk_1 = stream.read_uint64()
		instance.textures.arg = instance.texture_count
		instance.attributes.arg = instance.attribute_count
		instance.dependencies.arg = instance.textures
		instance.data_lib.arg = instance.attributes

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.context.version <= 15:
			stream.write_uint(instance.texture_count)
		if instance.context.version >= 17:
			stream.write_uint64(instance.texture_count)
		if instance.context.version <= 15:
			stream.write_uint(instance.attribute_count)
		if instance.context.version >= 17:
			stream.write_uint64(instance.attribute_count)
		ArrayPointer.to_stream(stream, instance.textures)
		ArrayPointer.to_stream(stream, instance.attributes)
		ForEachPointer.to_stream(stream, instance.dependencies)
		ForEachPointer.to_stream(stream, instance.data_lib)
		stream.write_uint64(instance.unk_0)
		stream.write_uint64(instance.unk_1)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		if instance.context.version <= 15:
			yield ('texture_count', Uint, (0, None))
		if instance.context.version >= 17:
			yield ('texture_count', Uint64, (0, None))
		if instance.context.version <= 15:
			yield ('attribute_count', Uint, (0, None))
		if instance.context.version >= 17:
			yield ('attribute_count', Uint64, (0, None))
		yield ('textures', ArrayPointer, (instance.texture_count, generated.formats.fgm.compound.TextureInfo.TextureInfo))
		yield ('attributes', ArrayPointer, (instance.attribute_count, generated.formats.fgm.compound.AttributeInfo.AttributeInfo))
		yield ('dependencies', ForEachPointer, (instance.textures, generated.formats.fgm.compound.DependencyInfo.DependencyInfo))
		yield ('data_lib', ForEachPointer, (instance.attributes, generated.formats.fgm.compound.AttribData.AttribData))
		yield ('unk_0', Uint64, (0, None))
		yield ('unk_1', Uint64, (0, None))

	def get_info_str(self, indent=0):
		return f'FgmHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* texture_count = {fmt_member(self.texture_count, indent+1)}'
		s += f'\n	* attribute_count = {fmt_member(self.attribute_count, indent+1)}'
		s += f'\n	* textures = {fmt_member(self.textures, indent+1)}'
		s += f'\n	* attributes = {fmt_member(self.attributes, indent+1)}'
		s += f'\n	* dependencies = {fmt_member(self.dependencies, indent+1)}'
		s += f'\n	* data_lib = {fmt_member(self.data_lib, indent+1)}'
		s += f'\n	* unk_0 = {fmt_member(self.unk_0, indent+1)}'
		s += f'\n	* unk_1 = {fmt_member(self.unk_1, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
