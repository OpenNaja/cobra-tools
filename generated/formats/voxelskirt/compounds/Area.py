from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64


class Area(BaseStruct):

	"""
	40 bytes
	"""

	__name__ = 'Area'

	_import_path = 'generated.formats.voxelskirt.compounds.Area'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into name list
		self.id = 0
		self.width_1 = 0
		self.height_1 = 0
		self.width_2 = 0
		self.height_2 = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'id', Uint64, (0, None), (False, None)
		yield 'width_1', Uint64, (0, None), (False, None)
		yield 'height_1', Uint64, (0, None), (False, None)
		yield 'width_2', Uint64, (0, None), (False, None)
		yield 'height_2', Uint64, (0, None), (False, None)
