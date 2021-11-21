import numpy
from generated.context import ContextReference


class ManiInfo:

	"""
	288 bytes for JWE / PZ
	312 bytes for PC
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.duration = 0.0

		# likely
		self.frame_count = 0
		self.b = 0

		# rest
		self.zeros_0 = numpy.zeros((6,), dtype=numpy.dtype('uint16'))
		self.c_0 = 0
		self.c_1 = 0
		self.name_count = 0

		# rest
		self.zeros_1 = numpy.zeros((3,), dtype=numpy.dtype('uint16'))
		self.e_2 = 0

		# always FF FF
		self.minus_1_a = 0
		self.e = 0
		self.extra_pc = numpy.zeros((5,), dtype=numpy.dtype('uint16'))
		self.g = 0

		# rest 228 bytes
		self.zeros_2 = numpy.zeros((57,), dtype=numpy.dtype('uint32'))

		# rest 14 bytes
		self.extra_zeros_pc = numpy.zeros((7,), dtype=numpy.dtype('uint16'))
		self.p_indices_c_0_min = 0
		self.p_indices_c_0_max = 0
		self.p_indices_c_1_min = 0
		self.p_indices_c_1_max = 0

		# always FF
		self.minus_1_b = 0

		# always 00
		self.zero = 0
		self.c_2 = 0
		self.c_3 = 0
		self.c_4 = 0
		self.c_5 = 0
		self.zeros_end = numpy.zeros((3,), dtype=numpy.dtype('uint16'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.duration = 0.0
		self.frame_count = 0
		self.b = 0
		self.zeros_0 = numpy.zeros((6,), dtype=numpy.dtype('uint16'))
		self.c_0 = 0
		self.c_1 = 0
		self.name_count = 0
		self.zeros_1 = numpy.zeros((3,), dtype=numpy.dtype('uint16'))
		self.e_2 = 0
		self.minus_1_a = 0
		self.e = 0
		if self.context.version == 18:
			self.extra_pc = numpy.zeros((5,), dtype=numpy.dtype('uint16'))
		self.g = 0
		self.zeros_2 = numpy.zeros((57,), dtype=numpy.dtype('uint32'))
		if self.context.version == 18:
			self.extra_zeros_pc = numpy.zeros((7,), dtype=numpy.dtype('uint16'))
		self.p_indices_c_0_min = 0
		self.p_indices_c_0_max = 0
		self.p_indices_c_1_min = 0
		self.p_indices_c_1_max = 0
		self.minus_1_b = 0
		self.zero = 0
		self.c_2 = 0
		self.c_3 = 0
		self.c_4 = 0
		self.c_5 = 0
		self.zeros_end = numpy.zeros((3,), dtype=numpy.dtype('uint16'))

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
		instance.duration = stream.read_float()
		instance.frame_count = stream.read_uint()
		instance.b = stream.read_uint()
		instance.zeros_0 = stream.read_ushorts((6,))
		instance.c_0 = stream.read_ushort()
		instance.c_1 = stream.read_ushort()
		instance.name_count = stream.read_ushort()
		instance.zeros_1 = stream.read_ushorts((3,))
		instance.e_2 = stream.read_ushort()
		instance.minus_1_a = stream.read_short()
		instance.e = stream.read_ushort()
		if instance.context.version == 18:
			instance.extra_pc = stream.read_ushorts((5,))
		instance.g = stream.read_ushort()
		instance.zeros_2 = stream.read_uints((57,))
		if instance.context.version == 18:
			instance.extra_zeros_pc = stream.read_ushorts((7,))
		instance.p_indices_c_0_min = stream.read_ubyte()
		instance.p_indices_c_0_max = stream.read_ubyte()
		instance.p_indices_c_1_min = stream.read_ubyte()
		instance.p_indices_c_1_max = stream.read_ubyte()
		instance.minus_1_b = stream.read_byte()
		instance.zero = stream.read_byte()
		instance.c_2 = stream.read_ubyte()
		instance.c_3 = stream.read_ubyte()
		instance.c_4 = stream.read_ubyte()
		instance.c_5 = stream.read_ubyte()
		instance.zeros_end = stream.read_ushorts((3,))

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_float(instance.duration)
		stream.write_uint(instance.frame_count)
		stream.write_uint(instance.b)
		stream.write_ushorts(instance.zeros_0)
		stream.write_ushort(instance.c_0)
		stream.write_ushort(instance.c_1)
		stream.write_ushort(instance.name_count)
		stream.write_ushorts(instance.zeros_1)
		stream.write_ushort(instance.e_2)
		stream.write_short(instance.minus_1_a)
		stream.write_ushort(instance.e)
		if instance.context.version == 18:
			stream.write_ushorts(instance.extra_pc)
		stream.write_ushort(instance.g)
		stream.write_uints(instance.zeros_2)
		if instance.context.version == 18:
			stream.write_ushorts(instance.extra_zeros_pc)
		stream.write_ubyte(instance.p_indices_c_0_min)
		stream.write_ubyte(instance.p_indices_c_0_max)
		stream.write_ubyte(instance.p_indices_c_1_min)
		stream.write_ubyte(instance.p_indices_c_1_max)
		stream.write_byte(instance.minus_1_b)
		stream.write_byte(instance.zero)
		stream.write_ubyte(instance.c_2)
		stream.write_ubyte(instance.c_3)
		stream.write_ubyte(instance.c_4)
		stream.write_ubyte(instance.c_5)
		stream.write_ushorts(instance.zeros_end)

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

	def get_info_str(self):
		return f'ManiInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* duration = {self.duration.__repr__()}'
		s += f'\n	* frame_count = {self.frame_count.__repr__()}'
		s += f'\n	* b = {self.b.__repr__()}'
		s += f'\n	* zeros_0 = {self.zeros_0.__repr__()}'
		s += f'\n	* c_0 = {self.c_0.__repr__()}'
		s += f'\n	* c_1 = {self.c_1.__repr__()}'
		s += f'\n	* name_count = {self.name_count.__repr__()}'
		s += f'\n	* zeros_1 = {self.zeros_1.__repr__()}'
		s += f'\n	* e_2 = {self.e_2.__repr__()}'
		s += f'\n	* minus_1_a = {self.minus_1_a.__repr__()}'
		s += f'\n	* e = {self.e.__repr__()}'
		s += f'\n	* extra_pc = {self.extra_pc.__repr__()}'
		s += f'\n	* g = {self.g.__repr__()}'
		s += f'\n	* zeros_2 = {self.zeros_2.__repr__()}'
		s += f'\n	* extra_zeros_pc = {self.extra_zeros_pc.__repr__()}'
		s += f'\n	* p_indices_c_0_min = {self.p_indices_c_0_min.__repr__()}'
		s += f'\n	* p_indices_c_0_max = {self.p_indices_c_0_max.__repr__()}'
		s += f'\n	* p_indices_c_1_min = {self.p_indices_c_1_min.__repr__()}'
		s += f'\n	* p_indices_c_1_max = {self.p_indices_c_1_max.__repr__()}'
		s += f'\n	* minus_1_b = {self.minus_1_b.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		s += f'\n	* c_2 = {self.c_2.__repr__()}'
		s += f'\n	* c_3 = {self.c_3.__repr__()}'
		s += f'\n	* c_4 = {self.c_4.__repr__()}'
		s += f'\n	* c_5 = {self.c_5.__repr__()}'
		s += f'\n	* zeros_end = {self.zeros_end.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
