import numpy
from generated.array import Array
from generated.formats.base.basic import Ubyte
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class BooleanData(MemStruct):

	"""
	8 bytes in log
	"""

	__name__ = 'BooleanData'

	_import_path = 'generated.formats.specdef.compounds.BooleanData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.value = 0
		self.default = 0
		self.unused = Array(self.context, 0, None, (0,), Ubyte)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.value = 0
		self.default = 0
		self.unused = numpy.zeros((6,), dtype=numpy.dtype('uint8'))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'value', Ubyte, (0, None), (False, None)
		yield 'default', Ubyte, (0, None), (False, None)
		yield 'unused', Array, (0, None, (6,), Ubyte), (False, None)

	def get_info_str(self, indent=0):
		return f'BooleanData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
