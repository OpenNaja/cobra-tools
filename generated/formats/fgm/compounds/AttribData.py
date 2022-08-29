import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Int
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class AttribData(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.value = Array((0,), Int, self.context, 0, None)
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
			Array.to_stream(stream, instance.value, (1,), Float, instance.context, 0, None)
		if instance.arg.dtype == 1:
			Array.to_stream(stream, instance.value, (2,), Float, instance.context, 0, None)
		if instance.arg.dtype == 2:
			Array.to_stream(stream, instance.value, (3,), Float, instance.context, 0, None)
		if instance.arg.dtype == 3:
			Array.to_stream(stream, instance.value, (4,), Float, instance.context, 0, None)
		if instance.arg.dtype == 5:
			Array.to_stream(stream, instance.value, (1,), Int, instance.context, 0, None)
		if instance.arg.dtype == 6:
			Array.to_stream(stream, instance.value, (1,), Int, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		if instance.arg.dtype == 0:
			yield 'value', Array, ((1,), Float, 0, None), (False, None)
		if instance.arg.dtype == 1:
			yield 'value', Array, ((2,), Float, 0, None), (False, None)
		if instance.arg.dtype == 2:
			yield 'value', Array, ((3,), Float, 0, None), (False, None)
		if instance.arg.dtype == 3:
			yield 'value', Array, ((4,), Float, 0, None), (False, None)
		if instance.arg.dtype == 5:
			yield 'value', Array, ((1,), Int, 0, None), (False, None)
		if instance.arg.dtype == 6:
			yield 'value', Array, ((1,), Int, 0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'AttribData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* value = {self.fmt_member(self.value, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
