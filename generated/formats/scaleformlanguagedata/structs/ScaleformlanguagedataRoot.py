from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.scaleformlanguagedata.imports import name_type_map


class ScaleformlanguagedataRoot(MemStruct):

	"""
	# PC - is maybe organized differently here
	PZ: 48 bytes
	"""

	__name__ = 'ScaleformlanguagedataRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.gfx_files_count = name_type_map['Uint64'](self.context, 0, None)
		self.fonts_count = name_type_map['Uint64'](self.context, 0, None)
		self.zero_2 = name_type_map['Uint64'](self.context, 0, None)
		self.zero_3 = name_type_map['Uint64'](self.context, 0, None)
		self.gfx_files = name_type_map['ArrayPointer'](self.context, self.gfx_files_count, name_type_map['GfxReference'])
		self.fonts = name_type_map['ArrayPointer'](self.context, self.fonts_count, name_type_map['FontInfo'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'gfx_files', name_type_map['ArrayPointer'], (None, name_type_map['GfxReference']), (False, None), (None, None)
		yield 'gfx_files_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'fonts', name_type_map['ArrayPointer'], (None, name_type_map['FontInfo']), (False, None), (None, None)
		yield 'fonts_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'zero_2', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'zero_3', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'gfx_files', name_type_map['ArrayPointer'], (instance.gfx_files_count, name_type_map['GfxReference']), (False, None)
		yield 'gfx_files_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'fonts', name_type_map['ArrayPointer'], (instance.fonts_count, name_type_map['FontInfo']), (False, None)
		yield 'fonts_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'zero_2', name_type_map['Uint64'], (0, None), (False, None)
		yield 'zero_3', name_type_map['Uint64'], (0, None), (False, None)
