from generated.formats.base.basic import Int
from generated.formats.voxelskirt.compounds.Material import Material


class EntityGroup(Material):

	"""
	32 bytes
	describes a list of instances of one entity
	"""

	__name__ = 'EntityGroup'

	_import_path = 'generated.formats.voxelskirt.compounds.EntityGroup'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# -1
		self.ff = 0

		# -1, 0 for PC
		self.ff_or_zero = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ff', Int, (0, None), (False, None)
		yield 'ff_or_zero', Int, (0, None), (False, None)
