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
		self.vertexdatasize = 0

		# 8 empty bytes
		self.ptr_1 = 0

		# PZ+, another 8 empty bytes
		self.unk_0 = 0
		self.facesdatasize = 0

		# 8 empty bytes
		self.ptr_2 = 0

		# PZ+, another 16 empty bytes
		self.unk_2 = numpy.zeros((2,), dtype=numpy.dtype('uint64'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if (self.context.version == 47) or (self.context.version == 39):
			self.skip_1 = numpy.zeros((2,), dtype=numpy.dtype('uint64'))
		self.vertexdatasize = 0
		self.ptr_1 = 0
		if self.context.version >= 48:
			self.unk_0 = 0
		self.facesdatasize = 0
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
		instance.vertexdatasize = stream.read_uint64()
		instance.ptr_1 = stream.read_uint64()
		if instance.context.version >= 48:
			instance.unk_0 = stream.read_uint64()
		instance.facesdatasize = stream.read_uint64()
		instance.ptr_2 = stream.read_uint64()
		if instance.context.version >= 48:
			instance.unk_2 = stream.read_uint64s((2,))

	@classmethod
	def write_fields(cls, stream, instance):
		if (instance.context.version == 47) or (instance.context.version == 39):
			stream.write_uint64s(instance.skip_1)
		stream.write_uint64(instance.vertexdatasize)
		stream.write_uint64(instance.ptr_1)
		if instance.context.version >= 48:
			stream.write_uint64(instance.unk_0)
		stream.write_uint64(instance.facesdatasize)
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

	def get_info_str(self):
		return f'BufferInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* skip_1 = {self.skip_1.__repr__()}'
		s += f'\n	* vertexdatasize = {self.vertexdatasize.__repr__()}'
		s += f'\n	* ptr_1 = {self.ptr_1.__repr__()}'
		s += f'\n	* unk_0 = {self.unk_0.__repr__()}'
		s += f'\n	* facesdatasize = {self.facesdatasize.__repr__()}'
		s += f'\n	* ptr_2 = {self.ptr_2.__repr__()}'
		s += f'\n	* unk_2 = {self.unk_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
