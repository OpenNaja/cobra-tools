from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.tex.imports import name_type_map


class Pc2TexBuffer(MemStruct):

	"""
	PC2 mime_version = 10 still, but completely different layout
	"""

	__name__ = 'Pc2TexBuffer'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.compression_type = name_type_map['DdsType'](self.context, 0, None)
		self.compression_pad = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])

		# x size in pixels
		self.width = name_type_map['Uint'](self.context, 0, None)

		# y size in pixels
		self.height = name_type_map['Uint'](self.context, 0, None)

		# may be depth
		self.depth = name_type_map['Uint'].from_value(1)
		self.num_tiles = name_type_map['Uint'].from_value(1)
		self.flag = name_type_map['Ubyte'].from_value(0)
		self.num_mips = name_type_map['Ubyte'](self.context, 0, None)
		self.num_mips_low = name_type_map['Ubyte'].from_value(7)
		self.num_mips_high = name_type_map['Ubyte'].from_value(9)
		self.weave_width = name_type_map['Uint'].from_value(256)
		self.weave_height = name_type_map['Uint'].from_value(256)
		self.can_weave = name_type_map['Uint'].from_value(1)
		self.buffer_size = name_type_map['Uint64'](self.context, 0, None)
		self.main = Array(self.context, 0, None, (0,), name_type_map['Pc2TexMip'])
		self.mip_maps = Array(self.context, 0, None, (0,), name_type_map['Pc2TexMip'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'compression_type', name_type_map['DdsType'], (0, None), (False, None), (None, None)
		yield 'compression_pad', Array, (0, None, (3,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'width', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'height', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'depth', name_type_map['Uint'], (0, None), (True, 1), (None, None)
		yield 'num_tiles', name_type_map['Uint'], (0, None), (True, 1), (None, None)
		yield 'flag', name_type_map['Ubyte'], (0, None), (False, 0), (None, None)
		yield 'num_mips', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'num_mips_low', name_type_map['Ubyte'], (0, None), (False, 7), (None, None)
		yield 'num_mips_high', name_type_map['Ubyte'], (0, None), (False, 9), (None, None)
		yield 'weave_width', name_type_map['Uint'], (0, None), (False, 256), (None, None)
		yield 'weave_height', name_type_map['Uint'], (0, None), (False, 256), (None, None)
		yield 'can_weave', name_type_map['Uint'], (0, None), (False, 1), (None, None)
		yield 'buffer_size', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'main', Array, (0, None, (2,), name_type_map['Pc2TexMip']), (False, None), (None, None)
		yield 'mip_maps', Array, (0, None, (14,), name_type_map['Pc2TexMip']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'compression_type', name_type_map['DdsType'], (0, None), (False, None)
		yield 'compression_pad', Array, (0, None, (3,), name_type_map['Ubyte']), (False, None)
		yield 'width', name_type_map['Uint'], (0, None), (False, None)
		yield 'height', name_type_map['Uint'], (0, None), (False, None)
		yield 'depth', name_type_map['Uint'], (0, None), (True, 1)
		yield 'num_tiles', name_type_map['Uint'], (0, None), (True, 1)
		yield 'flag', name_type_map['Ubyte'], (0, None), (False, 0)
		yield 'num_mips', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'num_mips_low', name_type_map['Ubyte'], (0, None), (False, 7)
		yield 'num_mips_high', name_type_map['Ubyte'], (0, None), (False, 9)
		yield 'weave_width', name_type_map['Uint'], (0, None), (False, 256)
		yield 'weave_height', name_type_map['Uint'], (0, None), (False, 256)
		yield 'can_weave', name_type_map['Uint'], (0, None), (False, 1)
		yield 'buffer_size', name_type_map['Uint64'], (0, None), (False, None)
		yield 'main', Array, (0, None, (2,), name_type_map['Pc2TexMip']), (False, None)
		yield 'mip_maps', Array, (0, None, (14,), name_type_map['Pc2TexMip']), (False, None)
