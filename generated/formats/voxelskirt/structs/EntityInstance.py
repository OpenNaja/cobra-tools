from generated.base_struct import BaseStruct
from generated.formats.voxelskirt.imports import name_type_map


class EntityInstance(BaseStruct):

	"""
	Describes the position of one instanced entity
	"""

	__name__ = 'EntityInstance'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.loc = name_type_map['Vector3F'](self.context, 0, None)
		self.z_rot = name_type_map['Float'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'loc', name_type_map['Vector3F'], (0, None), (False, None), (None, None)
		yield 'z_rot', name_type_map['Float'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'loc', name_type_map['Vector3F'], (0, None), (False, None)
		yield 'z_rot', name_type_map['Float'], (0, None), (False, None)
