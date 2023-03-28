from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float


class Vector3F(BaseStruct):

	__name__ = 'Vector3f'

	_import_key = 'voxelskirt.compounds.Vector3F'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('x', Float, (0, None), (False, None), (None, None))
		yield ('y', Float, (0, None), (False, None), (None, None))
		yield ('z', Float, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'x', Float, (0, None), (False, None)
		yield 'y', Float, (0, None), (False, None)
		yield 'z', Float, (0, None), (False, None)


Vector3F.init_attributes()
