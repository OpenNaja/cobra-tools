from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64
from generated.formats.voxelskirt.enums.VxlDtype import VxlDtype


class Layer(BaseStruct):

	"""
	32 bytes
	PZ and JWE only, describes a data layer image
	"""

	__name__ = 'Layer'

	_import_key = 'voxelskirt.compounds.Layer'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into name list
		self._id = 0
		self.dtype = VxlDtype(self.context, 0, None)

		# address of this data layer
		self._offset = 0

		# data size of this layer, in bytes
		self._data_size = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('_id', Uint64, (0, None), (False, None), (None, None))
		yield ('dtype', VxlDtype, (0, None), (False, None), (None, None))
		yield ('_offset', Uint64, (0, None), (False, None), (None, None))
		yield ('_data_size', Uint64, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield '_id', Uint64, (0, None), (False, None)
		yield 'dtype', VxlDtype, (0, None), (False, None)
		yield '_offset', Uint64, (0, None), (False, None)
		yield '_data_size', Uint64, (0, None), (False, None)


Layer.init_attributes()
