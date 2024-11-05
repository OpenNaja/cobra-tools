from generated.array import Array
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
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
		self.num_mips = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.unk_256_a = name_type_map['Uint'](self.context, 0, None)
		self.unk_256_b = name_type_map['Uint'](self.context, 0, None)
		self.unk_1 = name_type_map['Uint'](self.context, 0, None)
		self.buffer_size = name_type_map['Uint'](self.context, 0, None)
		self.unk_0 = name_type_map['Uint'](self.context, 0, None)
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
		yield 'num_mips', Array, (0, None, (4,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'unk_256_a', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_256_b', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'buffer_size', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_0', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'main', Array, (0, None, (2,), name_type_map['Pc2TexMip']), (False, None), (None, None)
		yield 'mips', Array, (0, None, (14,), name_type_map['Pc2TexMip']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'compression_type', name_type_map['DdsType'], (0, None), (False, None)
		yield 'compression_pad', Array, (0, None, (3,), name_type_map['Ubyte']), (False, None)
		yield 'width', name_type_map['Uint'], (0, None), (False, None)
		yield 'height', name_type_map['Uint'], (0, None), (False, None)
		yield 'depth', name_type_map['Uint'], (0, None), (True, 1)
		yield 'num_tiles', name_type_map['Uint'], (0, None), (True, 1)
		yield 'num_mips', Array, (0, None, (4,), name_type_map['Ubyte']), (False, None)
		yield 'unk_256_a', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_256_b', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'buffer_size', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_0', name_type_map['Uint'], (0, None), (False, None)
		yield 'main', Array, (0, None, (2,), name_type_map['Pc2TexMip']), (False, None)
		yield 'mips', Array, (0, None, (14,), name_type_map['Pc2TexMip']), (False, None)
