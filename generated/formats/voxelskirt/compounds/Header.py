from generated.formats.ovl_base.compounds.GenericHeader import GenericHeader
from generated.formats.voxelskirt.compounds.VoxelskirtRoot import VoxelskirtRoot


class Header(GenericHeader):

	"""
	Found at the beginning of every OVL file
	"""

	__name__ = 'Header'

	_import_key = 'voxelskirt.compounds.Header'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.info = VoxelskirtRoot(self.context, 0, None)
		if set_default:
			self.set_defaults()

	_attribute_list = GenericHeader._attribute_list + [
		('info', VoxelskirtRoot, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'info', VoxelskirtRoot, (0, None), (False, None)
