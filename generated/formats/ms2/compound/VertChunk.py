from source.formats.base.basic import fmt_member
import numpy
from generated.context import ContextReference
from generated.formats.ms2.bitfield.WeightsFlag import WeightsFlag


class VertChunk:

	"""
	JWE2 Biosyn: 16 bytes
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.flags = numpy.zeros((4,), dtype=numpy.dtype('uint8'))

		# scale: pack_base / 512, also added as offset
		self.pack_base = 0.0

		# byte offset from start of vert buffer in bytes
		self.vertex_offset = 0
		self.vertex_count = 0

		# determines if weights are used by this chunk
		self.weights_flag = WeightsFlag(self.context, 0, None)
		self.zero = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.flags = numpy.zeros((4,), dtype=numpy.dtype('uint8'))
		self.pack_base = 0.0
		self.vertex_offset = 0
		self.vertex_count = 0
		self.weights_flag = WeightsFlag(self.context, 0, None)
		self.zero = 0

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
		instance.flags = stream.read_ubytes((4,))
		instance.pack_base = stream.read_float()
		instance.vertex_offset = stream.read_uint()
		instance.vertex_count = stream.read_ubyte()
		instance.weights_flag = WeightsFlag.from_stream(stream, instance.context, 0, None)
		instance.zero = stream.read_ubyte()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_ubytes(instance.flags)
		stream.write_float(instance.pack_base)
		stream.write_uint(instance.vertex_offset)
		stream.write_ubyte(instance.vertex_count)
		WeightsFlag.to_stream(stream, instance.weights_flag)
		stream.write_ubyte(instance.zero)

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
		return f'VertChunk [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* flags = {fmt_member(self.flags, indent+1)}'
		s += f'\n	* pack_base = {fmt_member(self.pack_base, indent+1)}'
		s += f'\n	* vertex_offset = {fmt_member(self.vertex_offset, indent+1)}'
		s += f'\n	* vertex_count = {fmt_member(self.vertex_count, indent+1)}'
		s += f'\n	* weights_flag = {fmt_member(self.weights_flag, indent+1)}'
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
