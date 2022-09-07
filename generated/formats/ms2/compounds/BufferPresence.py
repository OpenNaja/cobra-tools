from generated.base_struct import BaseStruct
from generated.formats.base.basic import Int


class BufferPresence(BaseStruct):

	"""
	in DLA and JWE2, this can be a dependency to a model2stream
	"""

	__name__ = 'BufferPresence'

	_import_path = 'generated.formats.ms2.compounds.BufferPresence'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# -1 for a static buffer, 0 for streamed buffer; may be stream index
		self.pool_index = 0
		self.data_offset = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.pool_index = 0
		self.data_offset = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.pool_index = Int.from_stream(stream, instance.context, 0, None)
		instance.data_offset = Int.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Int.to_stream(stream, instance.pool_index)
		Int.to_stream(stream, instance.data_offset)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'pool_index', Int, (0, None), (False, None)
		yield 'data_offset', Int, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'BufferPresence [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
