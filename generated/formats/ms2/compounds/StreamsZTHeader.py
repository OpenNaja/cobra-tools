from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.ms2.compounds.InfoZTMemPool import InfoZTMemPool
from generated.formats.ovl_base.compounds.SmartPadding import SmartPadding


class StreamsZTHeader(BaseStruct):

	"""
	266 bytes ?
	very end of buffer 0 after the names list
	"""

	__name__ = 'StreamsZTHeader'

	_import_key = 'ms2.compounds.StreamsZTHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# sometimes 00 byte
		self.weird_padding = SmartPadding(self.context, 0, None)

		# ?
		self.unks = Array(self.context, 0, None, (0,), InfoZTMemPool)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('weird_padding', SmartPadding, (0, None), (False, None), (None, None))
		yield ('unks', Array, (0, None, (None,), InfoZTMemPool), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'weird_padding', SmartPadding, (0, None), (False, None)
		yield 'unks', Array, (0, None, (instance.arg.static_buffer_index,), InfoZTMemPool), (False, None)
