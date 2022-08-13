import numpy
from generated.array import Array
from generated.formats.base.basic import Uint
from generated.formats.ms2.compound.Matrix33 import Matrix33
from generated.formats.ms2.compound.Vector3 import Vector3
from generated.struct import StructBase


class BoundingBox(StructBase):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.rotation = 0

		# center of the box
		self.center = 0

		# total width
		self.extent = 0

		# probably padding
		self.zeros = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.rotation = Matrix33(self.context, 0, None)
		self.center = Vector3(self.context, 0, None)
		self.extent = Vector3(self.context, 0, None)
		if self.context.version == 32:
			self.zeros = numpy.zeros((3,), dtype=numpy.dtype('uint32'))

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
		instance.rotation = Matrix33.from_stream(stream, instance.context, 0, None)
		instance.center = Vector3.from_stream(stream, instance.context, 0, None)
		instance.extent = Vector3.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 32:
			instance.zeros = stream.read_uints((3,))

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Matrix33.to_stream(stream, instance.rotation)
		Vector3.to_stream(stream, instance.center)
		Vector3.to_stream(stream, instance.extent)
		if instance.context.version == 32:
			stream.write_uints(instance.zeros)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('rotation', Matrix33, (0, None))
		yield ('center', Vector3, (0, None))
		yield ('extent', Vector3, (0, None))
		if instance.context.version == 32:
			yield ('zeros', Array, ((3,), Uint, 0, None))

	def get_info_str(self, indent=0):
		return f'BoundingBox [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* rotation = {self.fmt_member(self.rotation, indent+1)}'
		s += f'\n	* center = {self.fmt_member(self.center, indent+1)}'
		s += f'\n	* extent = {self.fmt_member(self.extent, indent+1)}'
		s += f'\n	* zeros = {self.fmt_member(self.zeros, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
