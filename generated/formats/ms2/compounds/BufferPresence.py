from generated.base_struct import BaseStruct
from generated.formats.base.basic import Int


class BufferPresence(BaseStruct):

	"""
	in DLA and JWE2, this can be a dependency to a model2stream
	"""

	__name__ = 'BufferPresence'

	_import_key = 'ms2.compounds.BufferPresence'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# -1 for a static buffer, 0 for streamed buffer; may be stream index
		self.pool_index = 0
		self.data_offset = 0
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('pool_index', Int, (0, None), (False, None), None),
		('data_offset', Int, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'pool_index', Int, (0, None), (False, None)
		yield 'data_offset', Int, (0, None), (False, None)
