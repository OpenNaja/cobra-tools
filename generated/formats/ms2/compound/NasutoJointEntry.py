from generated.formats.base.basic import fmt_member
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.ms2.compound.Matrix33 import Matrix33
from generated.formats.ms2.compound.Vector4 import Vector4
from generated.struct import StructBase


class NasutoJointEntry(StructBase):

	"""
	60 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# index into bone list
		self.child = 0

		# index into bone list
		self.parent = 0

		# 0
		self.zero = 0

		# no clue what space this is in
		self.matrix = 0

		# seems to be degrees of freedom or something like that, possibly an ellipsoid
		self.vector = 0

		# 1
		self.one = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.child = 0
		self.parent = 0
		self.zero = 0
		self.matrix = Matrix33(self.context, 0, None)
		self.vector = Vector4(self.context, 0, None)
		self.one = 0

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
		instance.child = stream.read_ubyte()
		instance.parent = stream.read_ubyte()
		instance.zero = stream.read_ushort()
		instance.matrix = Matrix33.from_stream(stream, instance.context, 0, None)
		instance.vector = Vector4.from_stream(stream, instance.context, 0, None)
		instance.one = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_ubyte(instance.child)
		stream.write_ubyte(instance.parent)
		stream.write_ushort(instance.zero)
		Matrix33.to_stream(stream, instance.matrix)
		Vector4.to_stream(stream, instance.vector)
		stream.write_uint(instance.one)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('child', Ubyte, (0, None))
		yield ('parent', Ubyte, (0, None))
		yield ('zero', Ushort, (0, None))
		yield ('matrix', Matrix33, (0, None))
		yield ('vector', Vector4, (0, None))
		yield ('one', Uint, (0, None))

	def get_info_str(self, indent=0):
		return f'NasutoJointEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* child = {fmt_member(self.child, indent+1)}'
		s += f'\n	* parent = {fmt_member(self.parent, indent+1)}'
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		s += f'\n	* matrix = {fmt_member(self.matrix, indent+1)}'
		s += f'\n	* vector = {fmt_member(self.vector, indent+1)}'
		s += f'\n	* one = {fmt_member(self.one, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
