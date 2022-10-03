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

	_import_key = 'dds.structs.Header'

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

	_attribute_list = BaseStruct._attribute_list + [
		('header_string', FixedString, (4, None), (False, None), None),
		('size', Uint, (0, None), (False, 124), None),
		('flags', HeaderFlags, (0, None), (False, None), None),
		('height', Uint, (0, None), (False, None), None),
		('width', Uint, (0, None), (False, None), None),
		('linear_size', Uint, (0, None), (False, None), None),
		('depth', Uint, (0, None), (False, 1), None),
		('mipmap_count', Uint, (0, None), (False, None), None),
		('reserved_1', Array, (0, None, (11,), Uint), (False, None), None),
		('pixel_format', PixelFormat, (0, None), (False, None), None),
		('caps_1', Caps1, (0, None), (False, None), None),
		('caps_2', Caps2, (0, None), (False, None), None),
		('caps_3', Uint, (0, None), (False, None), None),
		('caps_4', Uint, (0, None), (False, None), None),
		('unused', Uint, (0, None), (False, None), None),
		('dx_10', Dxt10Header, (0, None), (False, None), True),
		]

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
