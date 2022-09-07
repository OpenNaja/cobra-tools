import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64


class ZTPreBones(BaseStruct):

	__name__ = 'ZTPreBones'

	_import_path = 'generated.formats.ms2.compounds.ZTPreBones'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zeros = Array(self.context, 0, None, (0,), Uint64)
		self.unks = Array(self.context, 0, None, (0,), Uint)
		self.unks_2 = Array(self.context, 0, None, (0,), Uint)
		self.floats = Array(self.context, 0, None, (0,), Float)
		self.unks_3 = Array(self.context, 0, None, (0,), Uint)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.zeros = numpy.zeros((2,), dtype=numpy.dtype('uint64'))
		self.unks = numpy.zeros((8,), dtype=numpy.dtype('uint32'))
		self.unks_2 = numpy.zeros((10,), dtype=numpy.dtype('uint32'))
		self.floats = numpy.zeros((4,), dtype=numpy.dtype('float32'))
		self.unks_3 = numpy.zeros((2,), dtype=numpy.dtype('uint32'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.zeros = Array.from_stream(stream, instance.context, 0, None, (2,), Uint64)
		instance.unks = Array.from_stream(stream, instance.context, 0, None, (8,), Uint)
		instance.unks_2 = Array.from_stream(stream, instance.context, 0, None, (10,), Uint)
		instance.floats = Array.from_stream(stream, instance.context, 0, None, (4,), Float)
		instance.unks_3 = Array.from_stream(stream, instance.context, 0, None, (2,), Uint)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.zeros, instance.context, 0, None, (2,), Uint64)
		Array.to_stream(stream, instance.unks, instance.context, 0, None, (8,), Uint)
		Array.to_stream(stream, instance.unks_2, instance.context, 0, None, (10,), Uint)
		Array.to_stream(stream, instance.floats, instance.context, 0, None, (4,), Float)
		Array.to_stream(stream, instance.unks_3, instance.context, 0, None, (2,), Uint)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'zeros', Array, (0, None, (2,), Uint64), (False, None)
		yield 'unks', Array, (0, None, (8,), Uint), (False, None)
		yield 'unks_2', Array, (0, None, (10,), Uint), (False, None)
		yield 'floats', Array, (0, None, (4,), Float), (False, None)
		yield 'unks_3', Array, (0, None, (2,), Uint), (False, None)

	def get_info_str(self, indent=0):
		return f'ZTPreBones [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
