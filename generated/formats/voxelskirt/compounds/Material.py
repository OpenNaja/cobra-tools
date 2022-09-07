from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64
from generated.formats.voxelskirt.compounds.DataSlot import DataSlot


class Material(BaseStruct):

	"""
	24 bytes
	"""

	__name__ = 'Material'

	_import_path = 'generated.formats.voxelskirt.compounds.Material'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.entity_instances = DataSlot(self.context, 0, Material._import_path_map["generated.formats.voxelskirt.compounds.EntityInstance"])

		# index into name list
		self.id = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.entity_instances = DataSlot(self.context, 0, Material._import_path_map["generated.formats.voxelskirt.compounds.EntityInstance"])
		self.id = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.entity_instances = DataSlot.from_stream(stream, instance.context, 0, Material._import_path_map["generated.formats.voxelskirt.compounds.EntityInstance"])
		instance.id = Uint64.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		DataSlot.to_stream(stream, instance.entity_instances)
		Uint64.to_stream(stream, instance.id)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'entity_instances', DataSlot, (0, Material._import_path_map["generated.formats.voxelskirt.compounds.EntityInstance"]), (False, None)
		yield 'id', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Material [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
