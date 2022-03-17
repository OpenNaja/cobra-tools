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

	def get_info_str(self):
		return f'NasutoJointEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* child = {self.child.__repr__()}'
		s += f'\n	* parent = {self.parent.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		s += f'\n	* matrix = {self.matrix.__repr__()}'
		s += f'\n	* vector = {self.vector.__repr__()}'
		s += f'\n	* one = {self.one.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
