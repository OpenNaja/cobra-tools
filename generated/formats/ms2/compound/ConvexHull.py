import numpy
from generated.context import ContextReference
from generated.formats.ms2.compound.Matrix33 import Matrix33
from generated.formats.ms2.compound.Vector3 import Vector3


class ConvexHull:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 16 for anubis: 4 hulls * 16 * 12 (size of vert)
		self.vertex_count = 0
		self.rotation = Matrix33(self.context, 0, None)

		# center of the box
		self.offset = Vector3(self.context, 0, None)

		# probably padding
		self.zeros = numpy.zeros((5,), dtype=numpy.dtype('uint32'))

		# probably padding
		self.zeros = numpy.zeros((2,), dtype=numpy.dtype('uint32'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.vertex_count = 0
		self.rotation = Matrix33(self.context, 0, None)
		self.offset = Vector3(self.context, 0, None)
		if self.context.version == 32:
			self.zeros = numpy.zeros((5,), dtype=numpy.dtype('uint32'))
		if ((self.context.version == 48) or (self.context.version == 50)) or (self.context.version == 51):
			self.zeros = numpy.zeros((2,), dtype=numpy.dtype('uint32'))

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
		instance.vertex_count = stream.read_uint()
		instance.rotation = Matrix33.from_stream(stream, instance.context, 0, None)
		instance.offset = Vector3.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 32:
			instance.zeros = stream.read_uints((5,))
		if ((instance.context.version == 48) or (instance.context.version == 50)) or (instance.context.version == 51):
			instance.zeros = stream.read_uints((2,))

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.vertex_count)
		Matrix33.to_stream(stream, instance.rotation)
		Vector3.to_stream(stream, instance.offset)
		if instance.context.version == 32:
			stream.write_uints(instance.zeros)
		if ((instance.context.version == 48) or (instance.context.version == 50)) or (instance.context.version == 51):
			stream.write_uints(instance.zeros)

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
		return f'ConvexHull [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* vertex_count = {self.vertex_count.__repr__()}'
		s += f'\n	* rotation = {self.rotation.__repr__()}'
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
