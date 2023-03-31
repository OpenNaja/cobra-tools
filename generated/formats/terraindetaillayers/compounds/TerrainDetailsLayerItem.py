from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TerrainDetailsLayerItem(MemStruct):

	"""
	# 88 bytes
	"""

	__name__ = 'TerrainDetailsLayerItem'

	_import_key = 'terraindetaillayers.compounds.TerrainDetailsLayerItem'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.info_count = 0
		self.float_1 = 0.0
		self.float_2 = 0.0
		self.float_3 = 0.0
		self.float_4 = 0.0
		self.float_5 = 0.0
		self.float_6 = 0.0
		self.unk_2 = 0
		self.detail_count = 0
		self.floata_1 = 0.0
		self.floata_2 = 0.0
		self.floata_3 = 0.0
		self.floata_4 = 0.0
		self.floata_5 = 0.0
		self.floata_6 = 0.0
		self.floata_7 = 0.0
		self.floata_8 = 0.0
		self.unk_3_flags = 0
		self.unk_4_found_as_1 = 0
		self.unk_5_as_0 = 0
		self.unk_6_as_0 = 0
		self.unk_7_as_0 = 0
		self.unk_8_as_0 = 0
		self.unk_9_as_0 = 0
		self.unk_a_as_0 = 0
		self.unk_b_as_0 = 0
		self.floatb_1 = 0.0
		self.floatb_2 = 0.0
		self.layer_name = Pointer(self.context, 0, ZString)
		self.info_list = ArrayPointer(self.context, self.info_count, TerrainDetailsLayerItem._import_map["terraindetaillayers.compounds.InfoStruct"])
		self.detail_list = ArrayPointer(self.context, self.detail_count, TerrainDetailsLayerItem._import_map["terraindetaillayers.compounds.DetailStruct"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('layer_name', Pointer, (0, ZString), (False, None), None)
		yield ('info_list', ArrayPointer, (None, None), (False, None), None)
		yield ('info_count', Uint, (0, None), (False, None), None)
		yield ('float_1', Float, (0, None), (False, None), None)
		yield ('float_2', Float, (0, None), (False, None), None)
		yield ('float_3', Float, (0, None), (False, None), None)
		yield ('float_4', Float, (0, None), (False, None), None)
		yield ('float_5', Float, (0, None), (False, None), None)
		yield ('float_6', Float, (0, None), (False, None), None)
		yield ('unk_2', Uint, (0, None), (False, None), None)
		yield ('detail_list', ArrayPointer, (None, None), (False, None), None)
		yield ('detail_count', Uint, (0, None), (False, None), None)
		yield ('floata_1', Float, (0, None), (False, None), None)
		yield ('floata_2', Float, (0, None), (False, None), None)
		yield ('floata_3', Float, (0, None), (False, None), None)
		yield ('floata_4', Float, (0, None), (False, None), None)
		yield ('floata_5', Float, (0, None), (False, None), None)
		yield ('floata_6', Float, (0, None), (False, None), None)
		yield ('floata_7', Float, (0, None), (False, None), None)
		yield ('floata_8', Float, (0, None), (False, None), None)
		yield ('unk_3_flags', Uint, (0, None), (False, None), None)
		yield ('unk_4_found_as_1', Uint, (0, None), (False, None), None)
		yield ('unk_5_as_0', Uint, (0, None), (False, None), None)
		yield ('unk_6_as_0', Uint, (0, None), (False, None), None)
		yield ('unk_7_as_0', Uint, (0, None), (False, None), None)
		yield ('unk_8_as_0', Uint, (0, None), (False, None), None)
		yield ('unk_9_as_0', Uint, (0, None), (False, None), None)
		yield ('unk_a_as_0', Uint, (0, None), (False, None), None)
		yield ('unk_b_as_0', Uint, (0, None), (False, None), None)
		yield ('floatb_1', Float, (0, None), (False, None), None)
		yield ('floatb_2', Float, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'layer_name', Pointer, (0, ZString), (False, None)
		yield 'info_list', ArrayPointer, (instance.info_count, TerrainDetailsLayerItem._import_map["terraindetaillayers.compounds.InfoStruct"]), (False, None)
		yield 'info_count', Uint, (0, None), (False, None)
		yield 'float_1', Float, (0, None), (False, None)
		yield 'float_2', Float, (0, None), (False, None)
		yield 'float_3', Float, (0, None), (False, None)
		yield 'float_4', Float, (0, None), (False, None)
		yield 'float_5', Float, (0, None), (False, None)
		yield 'float_6', Float, (0, None), (False, None)
		yield 'unk_2', Uint, (0, None), (False, None)
		yield 'detail_list', ArrayPointer, (instance.detail_count, TerrainDetailsLayerItem._import_map["terraindetaillayers.compounds.DetailStruct"]), (False, None)
		yield 'detail_count', Uint, (0, None), (False, None)
		yield 'floata_1', Float, (0, None), (False, None)
		yield 'floata_2', Float, (0, None), (False, None)
		yield 'floata_3', Float, (0, None), (False, None)
		yield 'floata_4', Float, (0, None), (False, None)
		yield 'floata_5', Float, (0, None), (False, None)
		yield 'floata_6', Float, (0, None), (False, None)
		yield 'floata_7', Float, (0, None), (False, None)
		yield 'floata_8', Float, (0, None), (False, None)
		yield 'unk_3_flags', Uint, (0, None), (False, None)
		yield 'unk_4_found_as_1', Uint, (0, None), (False, None)
		yield 'unk_5_as_0', Uint, (0, None), (False, None)
		yield 'unk_6_as_0', Uint, (0, None), (False, None)
		yield 'unk_7_as_0', Uint, (0, None), (False, None)
		yield 'unk_8_as_0', Uint, (0, None), (False, None)
		yield 'unk_9_as_0', Uint, (0, None), (False, None)
		yield 'unk_a_as_0', Uint, (0, None), (False, None)
		yield 'unk_b_as_0', Uint, (0, None), (False, None)
		yield 'floatb_1', Float, (0, None), (False, None)
		yield 'floatb_2', Float, (0, None), (False, None)


TerrainDetailsLayerItem.init_attributes()
