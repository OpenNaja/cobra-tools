from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.voxelskirt.compounds.DataSlot import DataSlot


class VoxelskirtRoot(MemStruct):

	"""
	# size varies according to game
	JWE2 - 120 bytes
	"""

	__name__ = 'VoxelskirtRoot'

	_import_key = 'voxelskirt.compounds.VoxelskirtRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zero = 0

		# total size of buffer data
		self._data_size = 0
		self.x = 0
		self.y = 0

		# multiply by x or y to get the actual dimension of skirt, eg 512px * 16.0 = 8192.0m
		self.scale = 0.0
		self.padding = 0

		# zero, for PC only
		self._height_offset = 0

		# x*y*4, for PC only
		self._weights_offset = 0
		self.layers = DataSlot(self.context, 0, VoxelskirtRoot._import_map["voxelskirt.compounds.Layer"])
		self.areas = DataSlot(self.context, 0, VoxelskirtRoot._import_map["voxelskirt.compounds.Area"])
		self.entity_groups = DataSlot(self.context, 0, VoxelskirtRoot._import_map["voxelskirt.compounds.EntityGroup"])
		self.materials = DataSlot(self.context, 0, VoxelskirtRoot._import_map["voxelskirt.compounds.Material"])
		self.names = DataSlot(self.context, 0, VoxelskirtRoot._import_map["voxelskirt.compounds.Name"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('zero', Uint64, (0, None), (True, 0), (None, None))
		yield ('_data_size', Uint64, (0, None), (False, None), (None, None))
		yield ('x', Uint64, (0, None), (False, None), (None, None))
		yield ('y', Uint64, (0, None), (False, None), (None, None))
		yield ('scale', Float, (0, None), (False, None), (None, None))
		yield ('padding', Uint, (0, None), (True, 0), (None, None))
		yield ('_height_offset', Uint64, (0, None), (False, None), (lambda context: context.version == 18, None))
		yield ('_weights_offset', Uint64, (0, None), (False, None), (lambda context: context.version == 18, None))
		yield ('layers', DataSlot, (0, VoxelskirtRoot._import_map["voxelskirt.compounds.Layer"]), (False, None), (lambda context: not (context.version == 18), None))
		yield ('areas', DataSlot, (0, VoxelskirtRoot._import_map["voxelskirt.compounds.Area"]), (False, None), (lambda context: not (context.version == 18), None))
		yield ('entity_groups', DataSlot, (0, VoxelskirtRoot._import_map["voxelskirt.compounds.EntityGroup"]), (False, None), (None, None))
		yield ('materials', DataSlot, (0, VoxelskirtRoot._import_map["voxelskirt.compounds.Material"]), (False, None), (None, None))
		yield ('names', DataSlot, (0, VoxelskirtRoot._import_map["voxelskirt.compounds.Name"]), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'zero', Uint64, (0, None), (True, 0)
		yield '_data_size', Uint64, (0, None), (False, None)
		yield 'x', Uint64, (0, None), (False, None)
		yield 'y', Uint64, (0, None), (False, None)
		yield 'scale', Float, (0, None), (False, None)
		yield 'padding', Uint, (0, None), (True, 0)
		if instance.context.version == 18:
			yield '_height_offset', Uint64, (0, None), (False, None)
			yield '_weights_offset', Uint64, (0, None), (False, None)
		if not (instance.context.version == 18):
			yield 'layers', DataSlot, (0, VoxelskirtRoot._import_map["voxelskirt.compounds.Layer"]), (False, None)
			yield 'areas', DataSlot, (0, VoxelskirtRoot._import_map["voxelskirt.compounds.Area"]), (False, None)
		yield 'entity_groups', DataSlot, (0, VoxelskirtRoot._import_map["voxelskirt.compounds.EntityGroup"]), (False, None)
		yield 'materials', DataSlot, (0, VoxelskirtRoot._import_map["voxelskirt.compounds.Material"]), (False, None)
		yield 'names', DataSlot, (0, VoxelskirtRoot._import_map["voxelskirt.compounds.Name"]), (False, None)
