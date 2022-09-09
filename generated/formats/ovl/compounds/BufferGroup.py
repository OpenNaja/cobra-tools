from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64


class BufferGroup(BaseStruct):

	"""
	32 bytes
	"""

	__name__ = 'BufferGroup'

	_import_key = 'ovl.compounds.BufferGroup'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# first buffer index
		self.buffer_offset = 0

		# number of buffers to grab
		self.buffer_count = 0

		# type of extension this entry is for
		self.ext_index = 0

		# which buffer index to populate
		self.buffer_index = 0

		# cumulative size of all buffers to grab
		self.size = 0

		# first data entry
		self.data_offset = 0

		# number of data entries to populate buffers into
		self.data_count = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'buffer_offset', Uint, (0, None), (False, None)
		yield 'buffer_count', Uint, (0, None), (False, None)
		yield 'ext_index', Uint, (0, None), (False, None)
		yield 'buffer_index', Uint, (0, None), (False, None)
		yield 'size', Uint64, (0, None), (False, None)
		yield 'data_offset', Uint, (0, None), (False, None)
		yield 'data_count', Uint, (0, None), (False, None)
