from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.voxelskirt.imports import name_type_map


class VoxelTerrainMaterialAssetPackagesRoot(MemStruct):

	"""
	# Currently only tested in PC2
	"""

	__name__ = 'VoxelTerrainMaterialAssetPackagesRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Could be padding.
		self.unk_1 = name_type_map['Uint64'].from_value(0)

		# It is not a list of strings
		self.package_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'package_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unk_1', name_type_map['Uint64'], (0, None), (False, 0), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'package_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unk_1', name_type_map['Uint64'], (0, None), (False, 0)
