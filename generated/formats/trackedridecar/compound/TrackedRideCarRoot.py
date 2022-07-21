from source.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.trackedridecar.compound.TrackedRideCarSub
import numpy
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class TrackedRideCarRoot(MemStruct):

	"""
	48 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default=False)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.sub_count = 0
		self.total_vecs_count = 0
		self.vec = numpy.zeros((3,), dtype=numpy.dtype('float32'))
		self.zero_0 = 0
		self.zero_1 = 0
		self.sub = ArrayPointer(self.context, self.sub_count, generated.formats.trackedridecar.compound.TrackedRideCarSub.TrackedRideCarSub)
		self.some_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.sub_count = 0
		self.total_vecs_count = 0
		self.vec = numpy.zeros((3,), dtype=numpy.dtype('float32'))
		self.zero_0 = 0
		self.zero_1 = 0
		self.sub = ArrayPointer(self.context, self.sub_count, generated.formats.trackedridecar.compound.TrackedRideCarSub.TrackedRideCarSub)
		self.some_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.sub = ArrayPointer.from_stream(stream, instance.context, instance.sub_count, generated.formats.trackedridecar.compound.TrackedRideCarSub.TrackedRideCarSub)
		instance.sub_count = stream.read_uint()
		instance.total_vecs_count = stream.read_uint()
		instance.vec = stream.read_floats((3,))
		instance.zero_0 = stream.read_uint()
		instance.some_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.zero_1 = stream.read_uint64()
		instance.sub.arg = instance.sub_count
		instance.some_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		ArrayPointer.to_stream(stream, instance.sub)
		stream.write_uint(instance.sub_count)
		stream.write_uint(instance.total_vecs_count)
		stream.write_floats(instance.vec)
		stream.write_uint(instance.zero_0)
		Pointer.to_stream(stream, instance.some_name)
		stream.write_uint64(instance.zero_1)

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
		return f'TrackedRideCarRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* sub = {fmt_member(self.sub, indent+1)}'
		s += f'\n	* sub_count = {fmt_member(self.sub_count, indent+1)}'
		s += f'\n	* total_vecs_count = {fmt_member(self.total_vecs_count, indent+1)}'
		s += f'\n	* vec = {fmt_member(self.vec, indent+1)}'
		s += f'\n	* zero_0 = {fmt_member(self.zero_0, indent+1)}'
		s += f'\n	* some_name = {fmt_member(self.some_name, indent+1)}'
		s += f'\n	* zero_1 = {fmt_member(self.zero_1, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
