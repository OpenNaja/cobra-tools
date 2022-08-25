import numpy
from generated.array import Array
from generated.formats.base.basic import Ubyte
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.tex.compounds.SizeInfoRaw import SizeInfoRaw


class SizeInfo(MemStruct):

	__name__ = 'SizeInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.data = SizeInfoRaw(self.context, 0, None)
		self.padding = Array((0,), Ubyte, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.data = SizeInfoRaw(self.context, 0, None)
		if ((not self.context.user_version.is_jwe) and (self.context.version == 20)) or (((not self.context.user_version.is_jwe) and (self.context.version >= 19)) or (self.context.user_version.is_jwe and (self.context.version == 20))):
			self.padding = numpy.zeros((320 - self.data.io_size,), dtype=numpy.dtype('uint8'))
		if self.context.user_version.is_jwe and (self.context.version == 19):
			self.padding = numpy.zeros((384 - self.data.io_size,), dtype=numpy.dtype('uint8'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.data = SizeInfoRaw.from_stream(stream, instance.context, 0, None)
		if ((not instance.context.user_version.is_jwe) and (instance.context.version == 20)) or (((not instance.context.user_version.is_jwe) and (instance.context.version >= 19)) or (instance.context.user_version.is_jwe and (instance.context.version == 20))):
			instance.padding = Array.from_stream(stream, instance.context, 0, None, (320 - instance.data.io_size,), Ubyte)
		if instance.context.user_version.is_jwe and (instance.context.version == 19):
			instance.padding = Array.from_stream(stream, instance.context, 0, None, (384 - instance.data.io_size,), Ubyte)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		SizeInfoRaw.to_stream(stream, instance.data)
		if ((not instance.context.user_version.is_jwe) and (instance.context.version == 20)) or (((not instance.context.user_version.is_jwe) and (instance.context.version >= 19)) or (instance.context.user_version.is_jwe and (instance.context.version == 20))):
			Array.to_stream(stream, instance.padding, (320 - instance.data.io_size,), Ubyte, instance.context, 0, None)
		if instance.context.user_version.is_jwe and (instance.context.version == 19):
			Array.to_stream(stream, instance.padding, (384 - instance.data.io_size,), Ubyte, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'data', SizeInfoRaw, (0, None), (False, None)
		if ((not instance.context.user_version.is_jwe) and (instance.context.version == 20)) or (((not instance.context.user_version.is_jwe) and (instance.context.version >= 19)) or (instance.context.user_version.is_jwe and (instance.context.version == 20))):
			yield 'padding', Array, ((320 - instance.data.io_size,), Ubyte, 0, None), (False, None)
		if instance.context.user_version.is_jwe and (instance.context.version == 19):
			yield 'padding', Array, ((384 - instance.data.io_size,), Ubyte, 0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'SizeInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* data = {self.fmt_member(self.data, indent+1)}'
		s += f'\n	* padding = {self.fmt_member(self.padding, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
