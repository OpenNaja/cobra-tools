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

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.data = Array((1,), ZStrPtr, self.context, 0, None)
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
			self.data = Array((1,), ZStrPtr, self.context, 0, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		if instance.arg == 0:
			instance.data = stream.read_bools((1,))
		if instance.arg == 1:
			instance.data = stream.read_floats((1,))
		if instance.arg == 2:
			instance.data = stream.read_ints((1,))
		if instance.arg == 3:
			instance.data = stream.read_uints((1,))
		if instance.arg == 4:
			instance.data = stream.read_floats((2,))
		if instance.arg == 5:
			instance.data = stream.read_floats((3,))
		if instance.arg == 6:
			instance.data = stream.read_floats((4,))
		if instance.arg == 7:
			instance.data = stream.read_ubytes((4,))
		if instance.arg == 8:
			instance.data = stream.read_floats((4,))
		if instance.arg == 9:
			instance.data = Array.from_stream(stream, (1,), ZStrPtr, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.arg == 0:
			stream.write_bools(instance.data)
		if instance.arg == 1:
			stream.write_floats(instance.data)
		if instance.arg == 2:
			stream.write_ints(instance.data)
		if instance.arg == 3:
			stream.write_uints(instance.data)
		if instance.arg == 4:
			stream.write_floats(instance.data)
		if instance.arg == 5:
			stream.write_floats(instance.data)
		if instance.arg == 6:
			stream.write_floats(instance.data)
		if instance.arg == 7:
			stream.write_ubytes(instance.data)
		if instance.arg == 8:
			stream.write_floats(instance.data)
		if instance.arg == 9:
			Array.to_stream(stream, instance.data, (1,), ZStrPtr, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		if instance.arg == 0:
			yield ('data', Array, ((1,), Bool, 0, None))
		if instance.arg == 1:
			yield ('data', Array, ((1,), Float, 0, None))
		if instance.arg == 2:
			yield ('data', Array, ((1,), Int, 0, None))
		if instance.arg == 3:
			yield ('data', Array, ((1,), Uint, 0, None))
		if instance.arg == 4:
			yield ('data', Array, ((2,), Float, 0, None))
		if instance.arg == 5:
			yield ('data', Array, ((3,), Float, 0, None))
		if instance.arg == 6:
			yield ('data', Array, ((4,), Float, 0, None))
		if instance.arg == 7:
			yield ('data', Array, ((4,), Ubyte, 0, None))
		if instance.arg == 8:
			yield ('data', Array, ((4,), Float, 0, None))
		if instance.arg == 9:
			yield ('data', Array, ((1,), ZStrPtr, 0, None))

	def get_info_str(self, indent=0):
		return f'ParamData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* data = {self.fmt_member(self.data, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
