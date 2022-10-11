import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.bnk.compounds.StreamInfo import StreamInfo


class BnkBufferData(BaseStruct):

	"""
	Buffer data of bnk files
	"""

	__name__ = 'BnkBufferData'

	_import_key = 'bnk.compounds.BnkBufferData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# data size of aux file of type b
		self.size_b = 0

		# 1, guess
		self.buffer_count = 0

		# 1 for PC, 2 for PZ, JWE1, 6 for ZTUAC
		self.count_2 = 0

		# variable
		self.stream_info_count = 0

		# 0
		self.zeros = Array(self.context, 0, None, (0,), Uint)

		# variable
		self.zeros_per_buffer = Array(self.context, 0, None, (0,), Uint64)

		# data
		self.stream_infos = Array(self.context, 0, None, (0,), StreamInfo)

		# data
		self.name = ''

		# ext format subtypes
		self.external_b_suffix = ''

		# ext format subtypes
		self.external_s_suffix = ''
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('size_b', Uint64, (0, None), (False, None), None),
		('buffer_count', Uint, (0, None), (False, None), None),
		('count_2', Uint, (0, None), (False, None), None),
		('stream_info_count', Uint, (0, None), (False, None), None),
		('zeros', Array, (0, None, (7,), Uint), (False, None), None),
		('zeros_per_buffer', Array, (0, None, (None, 2,), Uint64), (False, None), None),
		('stream_infos', Array, (0, None, (None,), StreamInfo), (False, None), None),
		('name', ZString, (0, None), (False, None), None),
		('external_b_suffix', ZString, (0, None), (False, None), True),
		('external_s_suffix', ZString, (0, None), (False, None), True),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'size_b', Uint64, (0, None), (False, None)
		yield 'buffer_count', Uint, (0, None), (False, None)
		yield 'count_2', Uint, (0, None), (False, None)
		yield 'stream_info_count', Uint, (0, None), (False, None)
		yield 'zeros', Array, (0, None, (7,), Uint), (False, None)
		yield 'zeros_per_buffer', Array, (0, None, (instance.buffer_count, 2,), Uint64), (False, None)
		yield 'stream_infos', Array, (0, None, (instance.stream_info_count,), StreamInfo), (False, None)
		yield 'name', ZString, (0, None), (False, None)
		if instance.buffer_count:
			yield 'external_b_suffix', ZString, (0, None), (False, None)
		if instance.stream_info_count:
			yield 'external_s_suffix', ZString, (0, None), (False, None)
