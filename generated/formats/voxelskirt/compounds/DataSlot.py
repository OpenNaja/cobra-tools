from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64


class DataSlot(BaseStruct):

	__name__ = 'DataSlot'

	_import_key = 'voxelskirt.compounds.DataSlot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# offset into buffer to start of data - only given if some count is nonzero
		self.offset = 0

		# count of data
		self.count = 0
		self.data = Array(self.context, 0, None, (0,), self.template)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('offset', Uint64, (0, None), (False, None), None),
		('count', Uint64, (0, None), (False, None), None),
		('data', Array, (0, None, (0,), None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'offset', Uint64, (0, None), (False, None)
		yield 'count', Uint64, (0, None), (False, None)
		yield 'data', Array, (0, None, (0,), instance.template), (False, None)
