import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint


class ZtVertBlockInfo(BaseStruct):

	"""
	16 bytes total
	"""

	__name__ = 'ZtVertBlockInfo'

	_import_key = 'ms2.compounds.ZtVertBlockInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.vertex_count = 0
		self.flags = Array(self.context, 0, None, (0,), Ubyte)
		self.zero = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('vertex_count', Uint, (0, None), (False, None), None)
		yield ('flags', Array, (0, None, (8,), Ubyte), (False, None), None)
		yield ('zero', Uint, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'vertex_count', Uint, (0, None), (False, None)
		yield 'flags', Array, (0, None, (8,), Ubyte), (False, None)
		yield 'zero', Uint, (0, None), (False, None)


ZtVertBlockInfo.init_attributes()
