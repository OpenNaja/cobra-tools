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

	_import_path = 'generated.formats.ms2.compounds.ZtVertBlockInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.vertex_count = 0
		self.flags = Array(self.context, 0, None, (0,), Ubyte)
		self.zero = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.vertex_count = 0
		self.flags = numpy.zeros((8,), dtype=numpy.dtype('uint8'))
		self.zero = 0

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'vertex_count', Uint, (0, None), (False, None)
		yield 'flags', Array, (0, None, (8,), Ubyte), (False, None)
		yield 'zero', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'ZtVertBlockInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
