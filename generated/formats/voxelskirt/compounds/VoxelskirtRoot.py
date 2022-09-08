from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.voxelskirt.compounds.DataSlot import DataSlot


class VoxelskirtRoot(MemStruct):

	"""
	# size varies according to game
	JWE2 - 120 bytes
	"""

	__name__ = 'VoxelskirtRoot'

	_import_path = 'generated.formats.voxelskirt.compounds.VoxelskirtRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zero = 0

		# total size of buffer data
		self.data_size = 0
		self.x = 0
		self.y = 0
		self.scale = 0.0
		self.padding = 0.0

		# zero, for PC only
		self.height_offset = 0

		# x*y*4, for PC only
		self.weights_offset = 0
		self.layers = DataSlot(self.context, 0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.Layer"])
		self.areas = DataSlot(self.context, 0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.Area"])
		self.entity_groups = DataSlot(self.context, 0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.EntityGroup"])
		self.materials = DataSlot(self.context, 0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.Material"])
		self.names = DataSlot(self.context, 0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.Name"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'zero', Uint64, (0, None), (False, None)
		yield 'data_size', Uint64, (0, None), (False, None)
		yield 'x', Uint64, (0, None), (False, None)
		yield 'y', Uint64, (0, None), (False, None)
		yield 'scale', Float, (0, None), (False, None)
		yield 'padding', Float, (0, None), (False, None)
		if instance.context.version == 18:
			yield 'height_offset', Uint64, (0, None), (False, None)
			yield 'weights_offset', Uint64, (0, None), (False, None)
		if not (instance.context.version == 18):
			yield 'layers', DataSlot, (0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.Layer"]), (False, None)
			yield 'areas', DataSlot, (0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.Area"]), (False, None)
		yield 'entity_groups', DataSlot, (0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.EntityGroup"]), (False, None)
		yield 'materials', DataSlot, (0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.Material"]), (False, None)
		yield 'names', DataSlot, (0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.Name"]), (False, None)

	def get_info_str(self, indent=0):
		return f'VoxelskirtRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
