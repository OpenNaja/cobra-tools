from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64


class Layer(BaseStruct):

	"""
	32 bytes
	PZ and JWE only, describes a data layer image
	"""

	__name__ = 'Layer'

	_import_path = 'generated.formats.voxelskirt.compounds.Layer'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into name list
		self.id = 0

		# 0 = ubyte, 2 = float
		self.dtype = 0

		# address of this data layer
		self.offset = 0

		# data size of this layer, in bytes
		self.dsize = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'id', Uint64, (0, None), (False, None)
		yield 'dtype', Uint64, (0, None), (False, None)
		yield 'offset', Uint64, (0, None), (False, None)
		yield 'dsize', Uint64, (0, None), (False, None)
