from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.spatialuitheme.imports import name_type_map


class SpatialUIThemeRoot(MemStruct):

	__name__ = 'SpatialUIThemeRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.spatial_u_i_theme_texture_count = name_type_map['Uint64'](self.context, 0, None)
		self.spatial_u_i_theme_texture_list = name_type_map['ArrayPointer'](self.context, self.spatial_u_i_theme_texture_count, name_type_map['SpatialUIThemeTexture'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'spatial_u_i_theme_texture_list', name_type_map['ArrayPointer'], (None, name_type_map['SpatialUIThemeTexture']), (False, None), (None, None)
		yield 'spatial_u_i_theme_texture_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'spatial_u_i_theme_texture_list', name_type_map['ArrayPointer'], (instance.spatial_u_i_theme_texture_count, name_type_map['SpatialUIThemeTexture']), (False, None)
		yield 'spatial_u_i_theme_texture_count', name_type_map['Uint64'], (0, None), (False, None)
