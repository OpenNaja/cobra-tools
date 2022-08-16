import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.ms2.compounds.Matrix33 import Matrix33
from generated.formats.ms2.compounds.Vector3 import Vector3


class ConvexHull(BaseStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 16 for anubis: 4 hulls * 16 * 12 (size of vert)
		self.vertex_count = 0
		self.rotation = Matrix33(self.context, 0, None)

		# center of the box
		self.offset = Vector3(self.context, 0, None)

		# probably padding
		self.zeros = numpy.zeros((2,), dtype=numpy.dtype('uint32'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.vertex_count = 0
		self.rotation = Matrix33(self.context, 0, None)
		self.offset = Vector3(self.context, 0, None)
		if self.context.version == 32:
			self.zeros = numpy.zeros((5,), dtype=numpy.dtype('uint32'))
		if ((self.context.version == 48) or (self.context.version == 50)) or (self.context.version == 51):
			self.zeros = numpy.zeros((2,), dtype=numpy.dtype('uint32'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.vertex_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.rotation = Matrix33.from_stream(stream, instance.context, 0, None)
		instance.offset = Vector3.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 32:
			instance.zeros = Array.from_stream(stream, instance.context, 0, None, (5,), Uint)
		if ((instance.context.version == 48) or (instance.context.version == 50)) or (instance.context.version == 51):
			instance.zeros = Array.from_stream(stream, instance.context, 0, None, (2,), Uint)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.vertex_count)
		Matrix33.to_stream(stream, instance.rotation)
		Vector3.to_stream(stream, instance.offset)
		if instance.context.version == 32:
			Array.to_stream(stream, instance.zeros, (5,), Uint, instance.context, 0, None)
		if ((instance.context.version == 48) or (instance.context.version == 50)) or (instance.context.version == 51):
			Array.to_stream(stream, instance.zeros, (2,), Uint, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'vertex_count', Uint, (0, None), (False, None)
		yield 'rotation', Matrix33, (0, None), (False, None)
		yield 'offset', Vector3, (0, None), (False, None)
		if instance.context.version == 32:
			yield 'zeros', Array, ((5,), Uint, 0, None), (False, None)
		if ((instance.context.version == 48) or (instance.context.version == 50)) or (instance.context.version == 51):
			yield 'zeros', Array, ((2,), Uint, 0, None), (False, None)

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
