import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.dds.basic import Uint
from generated.formats.dds.bitstructs.Caps1 import Caps1
from generated.formats.dds.bitstructs.Caps2 import Caps2
from generated.formats.dds.bitstructs.HeaderFlags import HeaderFlags
from generated.formats.dds.compounds.FixedString import FixedString
from generated.formats.dds.structs.Dxt10Header import Dxt10Header
from generated.formats.dds.structs.PixelFormat import PixelFormat


class Header(BaseStruct):

	__name__ = 'Header'

	_import_path = 'generated.formats.dds.structs.Header'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# DDS
		self.header_string = FixedString(self.context, 4, None)

		# Always 124 + 4 bytes for headerstring, header ends at 128.
		self.size = 124
		self.flags = HeaderFlags(self.context, 0, None)

		# The texture height.
		self.height = 0

		# The texture width.
		self.width = 0
		self.linear_size = 0
		self.depth = 1
		self.mipmap_count = 0
		self.reserved_1 = Array(self.context, 0, None, (0,), Uint)
		self.pixel_format = PixelFormat(self.context, 0, None)
		self.caps_1 = Caps1(self.context, 0, None)
		self.caps_2 = Caps2(self.context, 0, None)
		self.caps_3 = 0
		self.caps_4 = 0
		self.unused = 0
		self.dx_10 = Dxt10Header(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.header_string = FixedString(self.context, 4, None)
		self.size = 124
		self.flags = HeaderFlags(self.context, 0, None)
		self.height = 0
		self.width = 0
		self.linear_size = 0
		self.depth = 1
		self.mipmap_count = 0
		self.reserved_1 = numpy.zeros((11,), dtype=numpy.dtype('uint32'))
		self.pixel_format = PixelFormat(self.context, 0, None)
		self.caps_1 = Caps1(self.context, 0, None)
		self.caps_2 = Caps2(self.context, 0, None)
		self.caps_3 = 0
		self.caps_4 = 0
		self.unused = 0
		if self.pixel_format.four_c_c == 808540228:
			self.dx_10 = Dxt10Header(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.header_string = FixedString.from_stream(stream, instance.context, 4, None)
		instance.size = Uint.from_stream(stream, instance.context, 0, None)
		instance.flags = HeaderFlags.from_stream(stream, instance.context, 0, None)
		instance.height = Uint.from_stream(stream, instance.context, 0, None)
		instance.width = Uint.from_stream(stream, instance.context, 0, None)
		instance.linear_size = Uint.from_stream(stream, instance.context, 0, None)
		instance.depth = Uint.from_stream(stream, instance.context, 0, None)
		instance.mipmap_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.reserved_1 = Array.from_stream(stream, instance.context, 0, None, (11,), Uint)
		instance.pixel_format = PixelFormat.from_stream(stream, instance.context, 0, None)
		instance.caps_1 = Caps1.from_stream(stream, instance.context, 0, None)
		instance.caps_2 = Caps2.from_stream(stream, instance.context, 0, None)
		instance.caps_3 = Uint.from_stream(stream, instance.context, 0, None)
		instance.caps_4 = Uint.from_stream(stream, instance.context, 0, None)
		instance.unused = Uint.from_stream(stream, instance.context, 0, None)
		if instance.pixel_format.four_c_c == 808540228:
			instance.dx_10 = Dxt10Header.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		FixedString.to_stream(stream, instance.header_string)
		Uint.to_stream(stream, instance.size)
		HeaderFlags.to_stream(stream, instance.flags)
		Uint.to_stream(stream, instance.height)
		Uint.to_stream(stream, instance.width)
		Uint.to_stream(stream, instance.linear_size)
		Uint.to_stream(stream, instance.depth)
		Uint.to_stream(stream, instance.mipmap_count)
		Array.to_stream(stream, instance.reserved_1, instance.context, 0, None, (11,), Uint)
		PixelFormat.to_stream(stream, instance.pixel_format)
		Caps1.to_stream(stream, instance.caps_1)
		Caps2.to_stream(stream, instance.caps_2)
		Uint.to_stream(stream, instance.caps_3)
		Uint.to_stream(stream, instance.caps_4)
		Uint.to_stream(stream, instance.unused)
		if instance.pixel_format.four_c_c == 808540228:
			Dxt10Header.to_stream(stream, instance.dx_10)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'header_string', FixedString, (4, None), (False, None)
		yield 'size', Uint, (0, None), (False, 124)
		yield 'flags', HeaderFlags, (0, None), (False, None)
		yield 'height', Uint, (0, None), (False, None)
		yield 'width', Uint, (0, None), (False, None)
		yield 'linear_size', Uint, (0, None), (False, None)
		yield 'depth', Uint, (0, None), (False, 1)
		yield 'mipmap_count', Uint, (0, None), (False, None)
		yield 'reserved_1', Array, (0, None, (11,), Uint), (False, None)
		yield 'pixel_format', PixelFormat, (0, None), (False, None)
		yield 'caps_1', Caps1, (0, None), (False, None)
		yield 'caps_2', Caps2, (0, None), (False, None)
		yield 'caps_3', Uint, (0, None), (False, None)
		yield 'caps_4', Uint, (0, None), (False, None)
		yield 'unused', Uint, (0, None), (False, None)
		if instance.pixel_format.four_c_c == 808540228:
			yield 'dx_10', Dxt10Header, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Header [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
