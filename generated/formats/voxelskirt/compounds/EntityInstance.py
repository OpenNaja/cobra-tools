from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.voxelskirt.compounds.Vector3F import Vector3F


class EntityInstance(BaseStruct):

	"""
	Describes the position of one instanced entity
	"""

	__name__ = 'EntityInstance'

	_import_key = 'voxelskirt.compounds.EntityInstance'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.loc = Vector3F(self.context, 0, None)
		self.z_rot = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('loc', Vector3F, (0, None), (False, None), (None, None))
		yield ('z_rot', Float, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'loc', Vector3F, (0, None), (False, None)
		yield 'z_rot', Float, (0, None), (False, None)
