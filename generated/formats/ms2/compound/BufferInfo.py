from source.formats.base.basic import fmt_member
import numpy
from generated.context import ContextReference


class BufferInfo:

	"""
	Fragment data describing a MS2 buffer giving the size of the whole vertex and tri buffer.
	JWE: 48 bytes
	PZ: 56 bytes
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# JWE, 16 bytes of 00 padding
		self.skip_1 = numpy.zeros((2,), dtype=numpy.dtype('uint64'))
		self.vertex_buffer_size = 0

		# 8 empty bytes
		self.ptr_1 = 0

		# PZ+, another 8 empty bytes
		self.unk_0 = 0
		self.tris_buffer_size = 0

		# 8 empty bytes
		self.ptr_2 = 0

		# PZ+, another 16 empty bytes
		self.unk_2 = numpy.zeros((2,), dtype=numpy.dtype('uint64'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if (self.context.version == 47) or (self.context.version == 39):
			self.skip_1 = numpy.zeros((2,), dtype=numpy.dtype('uint64'))
		self.vertex_buffer_size = 0
		self.ptr_1 = 0
		if self.context.version >= 48:
			self.unk_0 = 0
		self.tris_buffer_size = 0
		self.ptr_2 = 0
		if self.context.version >= 48:
			self.unk_2 = numpy.zeros((2,), dtype=numpy.dtype('uint64'))

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
		if (instance.context.version == 47) or (instance.context.version == 39):
			instance.skip_1 = stream.read_uint64s((2,))
		instance.vertex_buffer_size = stream.read_uint64()
		instance.ptr_1 = stream.read_uint64()
		if instance.context.version >= 48:
			instance.unk_0 = stream.read_uint64()
		instance.tris_buffer_size = stream.read_uint64()
		instance.ptr_2 = stream.read_uint64()
		if instance.context.version >= 48:
			instance.unk_2 = stream.read_uint64s((2,))

	@classmethod
	def write_fields(cls, stream, instance):
		if (instance.context.version == 47) or (instance.context.version == 39):
			stream.write_uint64s(instance.skip_1)
		stream.write_uint64(instance.vertex_buffer_size)
		stream.write_uint64(instance.ptr_1)
		if instance.context.version >= 48:
			stream.write_uint64(instance.unk_0)
		stream.write_uint64(instance.tris_buffer_size)
		stream.write_uint64(instance.ptr_2)
		if instance.context.version >= 48:
			stream.write_uint64s(instance.unk_2)

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
		return f'BufferInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* skip_1 = {fmt_member(self.skip_1, indent+1)}'
		s += f'\n	* vertex_buffer_size = {fmt_member(self.vertex_buffer_size, indent+1)}'
		s += f'\n	* ptr_1 = {fmt_member(self.ptr_1, indent+1)}'
		s += f'\n	* unk_0 = {fmt_member(self.unk_0, indent+1)}'
		s += f'\n	* tris_buffer_size = {fmt_member(self.tris_buffer_size, indent+1)}'
		s += f'\n	* ptr_2 = {fmt_member(self.ptr_2, indent+1)}'
		s += f'\n	* unk_2 = {fmt_member(self.unk_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
