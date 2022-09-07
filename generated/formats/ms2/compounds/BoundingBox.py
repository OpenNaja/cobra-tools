import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.ms2.compounds.Matrix33 import Matrix33
from generated.formats.ms2.compounds.Vector3 import Vector3


class BoundingBox(BaseStruct):

	__name__ = 'BoundingBox'

	_import_path = 'generated.formats.ms2.compounds.BoundingBox'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.rotation = Matrix33(self.context, 0, None)

		# center of the box
		self.center = Vector3(self.context, 0, None)

		# total width
		self.extent = Vector3(self.context, 0, None)

		# probably padding
		self.zeros = Array(self.context, 0, None, (0,), Uint)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.rotation = Matrix33(self.context, 0, None)
		self.center = Vector3(self.context, 0, None)
		self.extent = Vector3(self.context, 0, None)
		if self.context.version == 32:
			self.zeros = numpy.zeros((3,), dtype=numpy.dtype('uint32'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.rotation = Matrix33.from_stream(stream, instance.context, 0, None)
		instance.center = Vector3.from_stream(stream, instance.context, 0, None)
		instance.extent = Vector3.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 32:
			instance.zeros = Array.from_stream(stream, instance.context, 0, None, (3,), Uint)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Matrix33.to_stream(stream, instance.rotation)
		Vector3.to_stream(stream, instance.center)
		Vector3.to_stream(stream, instance.extent)
		if instance.context.version == 32:
			Array.to_stream(stream, instance.zeros, instance.context, 0, None, (3,), Uint)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'rotation', Matrix33, (0, None), (False, None)
		yield 'center', Vector3, (0, None), (False, None)
		yield 'extent', Vector3, (0, None), (False, None)
		if instance.context.version == 32:
			yield 'zeros', Array, (0, None, (3,), Uint), (False, None)

	def get_info_str(self, indent=0):
		return f'BoundingBox [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
