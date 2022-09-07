from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.voxelskirt.compounds.Vector3F import Vector3F


class EntityInstance(BaseStruct):

	"""
	Describes the position of one instanced entity
	"""

	__name__ = 'EntityInstance'

	_import_path = 'generated.formats.voxelskirt.compounds.EntityInstance'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.loc = Vector3F(self.context, 0, None)
		self.z_rot = 0.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.loc = Vector3F(self.context, 0, None)
		self.z_rot = 0.0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.loc = Vector3F.from_stream(stream, instance.context, 0, None)
		instance.z_rot = Float.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Vector3F.to_stream(stream, instance.loc)
		Float.to_stream(stream, instance.z_rot)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'loc', Vector3F, (0, None), (False, None)
		yield 'z_rot', Float, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'EntityInstance [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
