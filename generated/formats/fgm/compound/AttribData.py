from source.formats.base.basic import fmt_member
import numpy
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class AttribData(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.value = numpy.zeros((1,), dtype=numpy.dtype('float32'))
		self.value = numpy.zeros((2,), dtype=numpy.dtype('float32'))
		self.value = numpy.zeros((3,), dtype=numpy.dtype('float32'))
		self.value = numpy.zeros((4,), dtype=numpy.dtype('float32'))
		self.value = numpy.zeros((1,), dtype=numpy.dtype('int32'))
		self.value = numpy.zeros((1,), dtype=numpy.dtype('int32'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
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
		if instance.arg.dtype == 0:
			instance.value = stream.read_floats((1,))
		if instance.arg.dtype == 1:
			instance.value = stream.read_floats((2,))
		if instance.arg.dtype == 2:
			instance.value = stream.read_floats((3,))
		if instance.arg.dtype == 3:
			instance.value = stream.read_floats((4,))
		if instance.arg.dtype == 5:
			instance.value = stream.read_ints((1,))
		if instance.arg.dtype == 6:
			instance.value = stream.read_ints((1,))

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.arg.dtype == 0:
			stream.write_floats(instance.value)
		if instance.arg.dtype == 1:
			stream.write_floats(instance.value)
		if instance.arg.dtype == 2:
			stream.write_floats(instance.value)
		if instance.arg.dtype == 3:
			stream.write_floats(instance.value)
		if instance.arg.dtype == 5:
			stream.write_ints(instance.value)
		if instance.arg.dtype == 6:
			stream.write_ints(instance.value)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'AttribData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* value = {fmt_member(self.value, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
