import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64


class Repeat(BaseStruct):

	__name__ = 'Repeat'

	_import_path = 'generated.formats.manis.compounds.Repeat'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zeros_0 = Array(self.context, 0, None, (0,), Uint64)

		# to be read sequentially starting after this array
		self.byte_size = 0
		self.zeros_1 = Array(self.context, 0, None, (0,), Uint64)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.zeros_0 = numpy.zeros((7,), dtype=numpy.dtype('uint64'))
		self.byte_size = 0
		self.zeros_1 = numpy.zeros((2,), dtype=numpy.dtype('uint64'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.zeros_0 = Array.from_stream(stream, instance.context, 0, None, (7,), Uint64)
		instance.byte_size = Uint64.from_stream(stream, instance.context, 0, None)
		instance.zeros_1 = Array.from_stream(stream, instance.context, 0, None, (2,), Uint64)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.zeros_0, Uint64)
		Uint64.to_stream(stream, instance.byte_size)
		Array.to_stream(stream, instance.zeros_1, Uint64)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'zeros_0', Array, (0, None, (7,), Uint64), (False, None)
		yield 'byte_size', Uint64, (0, None), (False, None)
		yield 'zeros_1', Array, (0, None, (2,), Uint64), (False, None)

	def get_info_str(self, indent=0):
		return f'Repeat [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
