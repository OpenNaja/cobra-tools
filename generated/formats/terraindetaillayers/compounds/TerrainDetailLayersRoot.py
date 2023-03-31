from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class TerrainDetailLayersRoot(MemStruct):

	"""
	# 16 bytes
	"""

	__name__ = 'TerrainDetailLayersRoot'

	_import_key = 'terraindetaillayers.compounds.TerrainDetailLayersRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.layer_count = 0
		self.layer_list = ArrayPointer(self.context, self.layer_count, TerrainDetailLayersRoot._import_map["terraindetaillayers.compounds.TerrainDetailsLayerItem"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('layer_list', ArrayPointer, (None, TerrainDetailLayersRoot._import_map["terraindetaillayers.compounds.TerrainDetailsLayerItem"]), (False, None), (None, None))
		yield ('layer_count', Uint64, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'layer_list', ArrayPointer, (instance.layer_count, TerrainDetailLayersRoot._import_map["terraindetaillayers.compounds.TerrainDetailsLayerItem"]), (False, None)
		yield 'layer_count', Uint64, (0, None), (False, None)


TerrainDetailLayersRoot.init_attributes()
