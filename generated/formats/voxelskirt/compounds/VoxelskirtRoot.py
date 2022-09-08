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

	def set_defaults(self):
		super().set_defaults()
		self.zero = 0
		self.data_size = 0
		self.x = 0
		self.y = 0
		self.scale = 0.0
		self.padding = 0.0
		if self.context.version == 18:
			self.height_offset = 0
			self.weights_offset = 0
		if not (self.context.version == 18):
			self.layers = DataSlot(self.context, 0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.Layer"])
			self.areas = DataSlot(self.context, 0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.Area"])
		self.entity_groups = DataSlot(self.context, 0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.EntityGroup"])
		self.materials = DataSlot(self.context, 0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.Material"])
		self.names = DataSlot(self.context, 0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.Name"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.zero = Uint64.from_stream(stream, instance.context, 0, None)
		instance.data_size = Uint64.from_stream(stream, instance.context, 0, None)
		instance.x = Uint64.from_stream(stream, instance.context, 0, None)
		instance.y = Uint64.from_stream(stream, instance.context, 0, None)
		instance.scale = Float.from_stream(stream, instance.context, 0, None)
		instance.padding = Float.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 18:
			instance.height_offset = Uint64.from_stream(stream, instance.context, 0, None)
			instance.weights_offset = Uint64.from_stream(stream, instance.context, 0, None)
		if not (instance.context.version == 18):
			instance.layers = DataSlot.from_stream(stream, instance.context, 0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.Layer"])
			instance.areas = DataSlot.from_stream(stream, instance.context, 0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.Area"])
		instance.entity_groups = DataSlot.from_stream(stream, instance.context, 0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.EntityGroup"])
		instance.materials = DataSlot.from_stream(stream, instance.context, 0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.Material"])
		instance.names = DataSlot.from_stream(stream, instance.context, 0, VoxelskirtRoot._import_path_map["generated.formats.voxelskirt.compounds.Name"])

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.zero)
		Uint64.to_stream(stream, instance.data_size)
		Uint64.to_stream(stream, instance.x)
		Uint64.to_stream(stream, instance.y)
		Float.to_stream(stream, instance.scale)
		Float.to_stream(stream, instance.padding)
		if instance.context.version == 18:
			Uint64.to_stream(stream, instance.height_offset)
			Uint64.to_stream(stream, instance.weights_offset)
		if not (instance.context.version == 18):
			DataSlot.to_stream(stream, instance.layers)
			DataSlot.to_stream(stream, instance.areas)
		DataSlot.to_stream(stream, instance.entity_groups)
		DataSlot.to_stream(stream, instance.materials)
		DataSlot.to_stream(stream, instance.names)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
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

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* zero = {self.fmt_member(self.zero, indent+1)}'
		s += f'\n	* data_size = {self.fmt_member(self.data_size, indent+1)}'
		s += f'\n	* x = {self.fmt_member(self.x, indent+1)}'
		s += f'\n	* y = {self.fmt_member(self.y, indent+1)}'
		s += f'\n	* scale = {self.fmt_member(self.scale, indent+1)}'
		s += f'\n	* padding = {self.fmt_member(self.padding, indent+1)}'
		s += f'\n	* height_offset = {self.fmt_member(self.height_offset, indent+1)}'
		s += f'\n	* weights_offset = {self.fmt_member(self.weights_offset, indent+1)}'
		s += f'\n	* layers = {self.fmt_member(self.layers, indent+1)}'
		s += f'\n	* areas = {self.fmt_member(self.areas, indent+1)}'
		s += f'\n	* entity_groups = {self.fmt_member(self.entity_groups, indent+1)}'
		s += f'\n	* materials = {self.fmt_member(self.materials, indent+1)}'
		s += f'\n	* names = {self.fmt_member(self.names, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
