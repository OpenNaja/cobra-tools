from source.formats.base.basic import fmt_member
import generated.formats.base.basic
import numpy
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class HabitatBoundaryPropRoot(MemStruct):

	"""
	144 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.u_0 = 0
		self.u_1 = 0
		self.floats = 0
		self.vec = 0
		self.u_2 = 0
		self.quat = 0
		self.name_a = 0
		self.name_b = 0
		self.name_c = 0
		self.name_d = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.u_0 = 0
		self.u_1 = 0
		self.floats = numpy.zeros((4, 4,), dtype=numpy.dtype('float32'))
		self.vec = numpy.zeros((3,), dtype=numpy.dtype('float32'))
		self.u_2 = 0
		self.quat = numpy.zeros((4,), dtype=numpy.dtype('float32'))
		self.name_a = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.name_b = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.name_c = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.name_d = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.u_0 = stream.read_uint64()
		instance.name_a = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.u_1 = stream.read_uint64()
		instance.name_b = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.name_c = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.floats = stream.read_floats((4, 4,))
		instance.name_d = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.vec = stream.read_floats((3,))
		instance.u_2 = stream.read_uint()
		instance.quat = stream.read_floats((4,))
		instance.name_a.arg = 0
		instance.name_b.arg = 0
		instance.name_c.arg = 0
		instance.name_d.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64(instance.u_0)
		Pointer.to_stream(stream, instance.name_a)
		stream.write_uint64(instance.u_1)
		Pointer.to_stream(stream, instance.name_b)
		Pointer.to_stream(stream, instance.name_c)
		stream.write_floats(instance.floats)
		Pointer.to_stream(stream, instance.name_d)
		stream.write_floats(instance.vec)
		stream.write_uint(instance.u_2)
		stream.write_floats(instance.quat)

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
		return f'HabitatBoundaryPropRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* u_0 = {fmt_member(self.u_0, indent+1)}'
		s += f'\n	* name_a = {fmt_member(self.name_a, indent+1)}'
		s += f'\n	* u_1 = {fmt_member(self.u_1, indent+1)}'
		s += f'\n	* name_b = {fmt_member(self.name_b, indent+1)}'
		s += f'\n	* name_c = {fmt_member(self.name_c, indent+1)}'
		s += f'\n	* floats = {fmt_member(self.floats, indent+1)}'
		s += f'\n	* name_d = {fmt_member(self.name_d, indent+1)}'
		s += f'\n	* vec = {fmt_member(self.vec, indent+1)}'
		s += f'\n	* u_2 = {fmt_member(self.u_2, indent+1)}'
		s += f'\n	* quat = {fmt_member(self.quat, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
