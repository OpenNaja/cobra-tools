from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.tex.imports import name_type_map


class Pc2TexMip(MemStruct):

	"""
	Data is stored per tile and this only stores the offset and size for the first tile
	To get to the next tile take the first offset and accumulate the sizes of all mips
	"""

	__name__ = 'Pc2TexMip'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.offset = name_type_map['Uint'](self.context, 0, None)
		self.size = name_type_map['Uint'](self.context, 0, None)
		self.num_weaves_x = name_type_map['Ushort'](self.context, 0, None)
		self.num_weaves_y = name_type_map['Ushort'](self.context, 0, None)
		self.do_weave = name_type_map['Short'](self.context, 0, None)
		self.ff = name_type_map['Short'].from_value(0)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'offset', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'size', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'num_weaves_x', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'num_weaves_y', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'do_weave', name_type_map['Short'], (0, None), (False, None), (None, None)
		yield 'ff', name_type_map['Short'], (0, None), (False, 0), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'offset', name_type_map['Uint'], (0, None), (False, None)
		yield 'size', name_type_map['Uint'], (0, None), (False, None)
		yield 'num_weaves_x', name_type_map['Ushort'], (0, None), (False, None)
		yield 'num_weaves_y', name_type_map['Ushort'], (0, None), (False, None)
		yield 'do_weave', name_type_map['Short'], (0, None), (False, None)
		yield 'ff', name_type_map['Short'], (0, None), (False, 0)
