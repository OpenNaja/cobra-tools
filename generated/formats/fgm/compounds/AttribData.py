import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Int
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class AttribData(MemStruct):

	__name__ = 'AttribData'

	_import_path = 'generated.formats.fgm.compounds.AttribData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.value = Array(self.context, 0, None, (0,), Int)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		if self.arg.dtype == 0:
			self.value = numpy.zeros((1,), dtype=numpy.dtype('float32'))
		if self.arg.dtype == 1:
			self.value = numpy.zeros((2,), dtype=numpy.dtype('float32'))
		if self.arg.dtype == 2:
			self.value = numpy.zeros((3,), dtype=numpy.dtype('float32'))
		if self.arg.dtype == 3:
			self.value = numpy.zeros((4,), dtype=numpy.dtype('float32'))
		if self.arg.dtype == 5:
			self.value = numpy.zeros((1,), dtype=numpy.dtype('int32'))
		if self.arg.dtype == 6:
			self.value = numpy.zeros((1,), dtype=numpy.dtype('int32'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		if instance.arg.dtype == 0:
			instance.value = Array.from_stream(stream, instance.context, 0, None, (1,), Float)
		if instance.arg.dtype == 1:
			instance.value = Array.from_stream(stream, instance.context, 0, None, (2,), Float)
		if instance.arg.dtype == 2:
			instance.value = Array.from_stream(stream, instance.context, 0, None, (3,), Float)
		if instance.arg.dtype == 3:
			instance.value = Array.from_stream(stream, instance.context, 0, None, (4,), Float)
		if instance.arg.dtype == 5:
			instance.value = Array.from_stream(stream, instance.context, 0, None, (1,), Int)
		if instance.arg.dtype == 6:
			instance.value = Array.from_stream(stream, instance.context, 0, None, (1,), Int)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.arg.dtype == 0:
			Array.to_stream(stream, instance.value, Float)
		if instance.arg.dtype == 1:
			Array.to_stream(stream, instance.value, Float)
		if instance.arg.dtype == 2:
			Array.to_stream(stream, instance.value, Float)
		if instance.arg.dtype == 3:
			Array.to_stream(stream, instance.value, Float)
		if instance.arg.dtype == 5:
			Array.to_stream(stream, instance.value, Int)
		if instance.arg.dtype == 6:
			Array.to_stream(stream, instance.value, Int)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.arg.dtype == 0:
			yield 'value', Array, (0, None, (1,), Float), (False, None)
		if instance.arg.dtype == 1:
			yield 'value', Array, (0, None, (2,), Float), (False, None)
		if instance.arg.dtype == 2:
			yield 'value', Array, (0, None, (3,), Float), (False, None)
		if instance.arg.dtype == 3:
			yield 'value', Array, (0, None, (4,), Float), (False, None)
		if instance.arg.dtype == 5:
			yield 'value', Array, (0, None, (1,), Int), (False, None)
		if instance.arg.dtype == 6:
			yield 'value', Array, (0, None, (1,), Int), (False, None)

	def get_info_str(self, indent=0):
		return f'AttribData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
