import numpy
from generated.array import Array
from generated.formats.base.basic import Uint
from generated.formats.ms2.compound.Matrix33 import Matrix33
from generated.formats.ms2.compound.Vector3 import Vector3
from generated.struct import StructBase


class ConvexHull(StructBase):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 16 for anubis: 4 hulls * 16 * 12 (size of vert)
		self.vertex_count = 0
		self.rotation = 0

		# center of the box
		self.offset = 0

		# probably padding
		self.zeros = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
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
		super().read_fields(stream, instance)
		instance.vertex_count = stream.read_uint()
		instance.rotation = Matrix33.from_stream(stream, instance.context, 0, None)
		instance.offset = Vector3.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 32:
			instance.zeros = stream.read_uints((5,))
		if ((instance.context.version == 48) or (instance.context.version == 50)) or (instance.context.version == 51):
			instance.zeros = stream.read_uints((2,))

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.vertex_count)
		Matrix33.to_stream(stream, instance.rotation)
		Vector3.to_stream(stream, instance.offset)
		if instance.context.version == 32:
			stream.write_uints(instance.zeros)
		if ((instance.context.version == 48) or (instance.context.version == 50)) or (instance.context.version == 51):
			stream.write_uints(instance.zeros)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('vertex_count', Uint, (0, None))
		yield ('rotation', Matrix33, (0, None))
		yield ('offset', Vector3, (0, None))
		if instance.context.version == 32:
			yield ('zeros', Array, ((5,), Uint, 0, None))
		if ((instance.context.version == 48) or (instance.context.version == 50)) or (instance.context.version == 51):
			yield ('zeros', Array, ((2,), Uint, 0, None))

	def get_info_str(self, indent=0):
		return f'ConvexHull [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* vertex_count = {self.fmt_member(self.vertex_count, indent+1)}'
		s += f'\n	* rotation = {self.fmt_member(self.rotation, indent+1)}'
		s += f'\n	* offset = {self.fmt_member(self.offset, indent+1)}'
		s += f'\n	* zeros = {self.fmt_member(self.zeros, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
