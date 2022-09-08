import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Int
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.basic import Bool
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.renderparameters.compounds.ZStrPtr import ZStrPtr


class ParamData(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'ParamData'

	_import_path = 'generated.formats.renderparameters.compounds.ParamData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.data = Array(self.context, 0, None, (0,), ZStrPtr)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		if self.arg == 0:
			self.data = numpy.zeros((1,), dtype=numpy.dtype('bool'))
		if self.arg == 1:
			self.data = numpy.zeros((1,), dtype=numpy.dtype('float32'))
		if self.arg == 2:
			self.data = numpy.zeros((1,), dtype=numpy.dtype('int32'))
		if self.arg == 3:
			self.data = numpy.zeros((1,), dtype=numpy.dtype('uint32'))
		if self.arg == 4:
			self.data = numpy.zeros((2,), dtype=numpy.dtype('float32'))
		if self.arg == 5:
			self.data = numpy.zeros((3,), dtype=numpy.dtype('float32'))
		if self.arg == 6:
			self.data = numpy.zeros((4,), dtype=numpy.dtype('float32'))
		if self.arg == 7:
			self.data = numpy.zeros((4,), dtype=numpy.dtype('uint8'))
		if self.arg == 8:
			self.data = numpy.zeros((4,), dtype=numpy.dtype('float32'))
		if self.arg == 9:
			self.data = Array(self.context, 0, None, (1,), ZStrPtr)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.arg == 0:
			yield 'data', Array, (0, None, (1,), Bool), (False, None)
		if instance.arg == 1:
			yield 'data', Array, (0, None, (1,), Float), (False, None)
		if instance.arg == 2:
			yield 'data', Array, (0, None, (1,), Int), (False, None)
		if instance.arg == 3:
			yield 'data', Array, (0, None, (1,), Uint), (False, None)
		if instance.arg == 4:
			yield 'data', Array, (0, None, (2,), Float), (False, None)
		if instance.arg == 5:
			yield 'data', Array, (0, None, (3,), Float), (False, None)
		if instance.arg == 6:
			yield 'data', Array, (0, None, (4,), Float), (False, None)
		if instance.arg == 7:
			yield 'data', Array, (0, None, (4,), Ubyte), (False, None)
		if instance.arg == 8:
			yield 'data', Array, (0, None, (4,), Float), (False, None)
		if instance.arg == 9:
			yield 'data', Array, (0, None, (1,), ZStrPtr), (False, None)

	def get_info_str(self, indent=0):
		return f'ParamData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
