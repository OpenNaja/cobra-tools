from source.formats.base.basic import fmt_member
from generated.context import ContextReference
from generated.formats.ms2.compound.Matrix33 import Matrix33
from generated.formats.ms2.compound.Vector4 import Vector4


class NasutoJointEntry:

	"""
	60 bytes
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
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
		self.matrix = Matrix33(self.context, 0, None)

		# seems to be degrees of freedom or something like that, possibly an ellipsoid
		self.vector = Vector4(self.context, 0, None)

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
		instance.child = stream.read_ubyte()
		instance.parent = stream.read_ubyte()
		instance.zero = stream.read_ushort()
		instance.matrix = Matrix33.from_stream(stream, instance.context, 0, None)
		instance.vector = Vector4.from_stream(stream, instance.context, 0, None)
		instance.one = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_ubyte(instance.child)
		stream.write_ubyte(instance.parent)
		stream.write_ushort(instance.zero)
		Matrix33.to_stream(stream, instance.matrix)
		Vector4.to_stream(stream, instance.vector)
		stream.write_uint(instance.one)

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
		return f'NasutoJointEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
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
