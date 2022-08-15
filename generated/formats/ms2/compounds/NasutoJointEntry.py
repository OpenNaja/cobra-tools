from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.ms2.compounds.Matrix33 import Matrix33
from generated.formats.ms2.compounds.Vector4 import Vector4


class NasutoJointEntry(BaseStruct):

	"""
	60 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into bone list
		self.child = 0

		# index into bone list
		self.parent = 0

		# 0
		self.zero = 0

		# no clue what space this is in
		self.matrix = Matrix33(self.context, 0, None)

		# seems to be degrees of freedom or something like that, possibly an ellipsoid
		self.vector = Vector4(self.context, 0, None)

		# 1
		self.one = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.child = 0
		self.parent = 0
		self.zero = 0
		self.matrix = Matrix33(self.context, 0, None)
		self.vector = Vector4(self.context, 0, None)
		self.one = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.child = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.parent = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.zero = Ushort.from_stream(stream, instance.context, 0, None)
		instance.matrix = Matrix33.from_stream(stream, instance.context, 0, None)
		instance.vector = Vector4.from_stream(stream, instance.context, 0, None)
		instance.one = Uint.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Ubyte.to_stream(stream, instance.child)
		Ubyte.to_stream(stream, instance.parent)
		Ushort.to_stream(stream, instance.zero)
		Matrix33.to_stream(stream, instance.matrix)
		Vector4.to_stream(stream, instance.vector)
		Uint.to_stream(stream, instance.one)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'child', Ubyte, (0, None)
		yield 'parent', Ubyte, (0, None)
		yield 'zero', Ushort, (0, None)
		yield 'matrix', Matrix33, (0, None)
		yield 'vector', Vector4, (0, None)
		yield 'one', Uint, (0, None)

	def get_info_str(self, indent=0):
		return f'NasutoJointEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* child = {self.fmt_member(self.child, indent+1)}'
		s += f'\n	* parent = {self.fmt_member(self.parent, indent+1)}'
		s += f'\n	* zero = {self.fmt_member(self.zero, indent+1)}'
		s += f'\n	* matrix = {self.fmt_member(self.matrix, indent+1)}'
		s += f'\n	* vector = {self.fmt_member(self.vector, indent+1)}'
		s += f'\n	* one = {self.fmt_member(self.one, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
