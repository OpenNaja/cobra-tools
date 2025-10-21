from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.voxelskirt.imports import name_type_map


class VoxelTerrainMaterialLayerSpecRoot(MemStruct):

	"""
	# Currently only tested in PC2
	"""

	__name__ = 'VoxelTerrainMaterialLayerSpecRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# unknown
		self.tile_size = name_type_map['Float'](self.context, 0, None)

		# invisible value
		self.float_2 = name_type_map['Float'](self.context, 0, None)

		# Not entirely sure, check again
		self.flags = name_type_map['Uint'](self.context, 0, None)

		# invisible value
		self.float_3 = name_type_map['Float'](self.context, 0, None)
		self.parallax = name_type_map['Float'](self.context, 0, None)
		self.macro_amount = name_type_map['Float'](self.context, 0, None)
		self.water_permeability = name_type_map['Float'](self.context, 0, None)
		self.macro_albedo = name_type_map['Float'](self.context, 0, None)
		self.detail_normal = name_type_map['Float'](self.context, 0, None)
		self.macro_roughness = name_type_map['Float'](self.context, 0, None)
		self.macro_full = name_type_map['Float'](self.context, 0, None)
		self.smoothness = name_type_map['Float'](self.context, 0, None)

		# invisible value
		self.float_10 = name_type_map['Float'](self.context, 0, None)

		# invisible value
		self.float_11 = name_type_map['Float'](self.context, 0, None)

		# Invisible value, note: could be the brush name?
		self.unknown_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'unknown_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'tile_size', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'float_2', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'flags', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'float_3', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'parallax', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'macro_amount', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'water_permeability', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'macro_albedo', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'detail_normal', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'macro_roughness', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'macro_full', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'smoothness', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'float_10', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'float_11', name_type_map['Float'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unknown_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'tile_size', name_type_map['Float'], (0, None), (False, None)
		yield 'float_2', name_type_map['Float'], (0, None), (False, None)
		yield 'flags', name_type_map['Uint'], (0, None), (False, None)
		yield 'float_3', name_type_map['Float'], (0, None), (False, None)
		yield 'parallax', name_type_map['Float'], (0, None), (False, None)
		yield 'macro_amount', name_type_map['Float'], (0, None), (False, None)
		yield 'water_permeability', name_type_map['Float'], (0, None), (False, None)
		yield 'macro_albedo', name_type_map['Float'], (0, None), (False, None)
		yield 'detail_normal', name_type_map['Float'], (0, None), (False, None)
		yield 'macro_roughness', name_type_map['Float'], (0, None), (False, None)
		yield 'macro_full', name_type_map['Float'], (0, None), (False, None)
		yield 'smoothness', name_type_map['Float'], (0, None), (False, None)
		yield 'float_10', name_type_map['Float'], (0, None), (False, None)
		yield 'float_11', name_type_map['Float'], (0, None), (False, None)
