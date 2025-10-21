from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.spatialuitheme.imports import name_type_map


class SpatialUIThemeTexture(MemStruct):

	__name__ = 'SpatialUITheme_Texture'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.spatial_u_i_theme_texture_id = name_type_map['Uint64'](self.context, 0, None)
		self.spatial_u_i_theme_colour = name_type_map['ByteColor'](self.context, 0, None)
		self.spatial_u_i_theme_colour_unknown = name_type_map['Int'](self.context, 0, None)
		self.spatial_u_i_theme_texture_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'spatial_u_i_theme_texture_id', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'spatial_u_i_theme_texture_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'spatial_u_i_theme_colour', name_type_map['ByteColor'], (0, None), (False, None), (None, None)
		yield 'spatial_u_i_theme_colour_unknown', name_type_map['Int'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'spatial_u_i_theme_texture_id', name_type_map['Uint64'], (0, None), (False, None)
		yield 'spatial_u_i_theme_texture_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'spatial_u_i_theme_colour', name_type_map['ByteColor'], (0, None), (False, None)
		yield 'spatial_u_i_theme_colour_unknown', name_type_map['Int'], (0, None), (False, None)
