from source.formats.base.basic import fmt_member
from generated.context import ContextReference
from generated.formats.ms2.compound.Vector3 import Vector3
from generated.formats.ms2.compound.Vector4 import Vector4


class PosChunk:

	"""
	used in JWE2 Biosyn
	64 bytes
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# the smallest coordinates across all axes
		self.bounds_min = Vector3(self.context, 0, None)
		self.u_0 = 0
		self.u_1 = 0

		# the biggest coordinates across all axes
		self.bounds_max = Vector3(self.context, 0, None)
		self.tris_offset = 0

		# can be 0,0,0, no obvious range
		self.loc = Vector3(self.context, 0, None)

		# can be 1, 0, 0, 0, the always in range -1, +1
		self.rot = Vector4(self.context, 0, None)
		self.u_2 = 0
		self.u_3 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.bounds_min = Vector3(self.context, 0, None)
		self.u_0 = 0
		self.u_1 = 0
		self.bounds_max = Vector3(self.context, 0, None)
		self.tris_offset = 0
		self.loc = Vector3(self.context, 0, None)
		self.rot = Vector4(self.context, 0, None)
		self.u_2 = 0
		self.u_3 = 0

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
		instance.bounds_min = Vector3.from_stream(stream, instance.context, 0, None)
		instance.u_0 = stream.read_ushort()
		instance.u_1 = stream.read_ushort()
		instance.bounds_max = Vector3.from_stream(stream, instance.context, 0, None)
		instance.tris_offset = stream.read_uint()
		instance.loc = Vector3.from_stream(stream, instance.context, 0, None)
		instance.rot = Vector4.from_stream(stream, instance.context, 0, None)
		instance.u_2 = stream.read_ushort()
		instance.u_3 = stream.read_ushort()

	@classmethod
	def write_fields(cls, stream, instance):
		Vector3.to_stream(stream, instance.bounds_min)
		stream.write_ushort(instance.u_0)
		stream.write_ushort(instance.u_1)
		Vector3.to_stream(stream, instance.bounds_max)
		stream.write_uint(instance.tris_offset)
		Vector3.to_stream(stream, instance.loc)
		Vector4.to_stream(stream, instance.rot)
		stream.write_ushort(instance.u_2)
		stream.write_ushort(instance.u_3)

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
		return f'PosChunk [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* bounds_min = {fmt_member(self.bounds_min, indent+1)}'
		s += f'\n	* u_0 = {fmt_member(self.u_0, indent+1)}'
		s += f'\n	* u_1 = {fmt_member(self.u_1, indent+1)}'
		s += f'\n	* bounds_max = {fmt_member(self.bounds_max, indent+1)}'
		s += f'\n	* tris_offset = {fmt_member(self.tris_offset, indent+1)}'
		s += f'\n	* loc = {fmt_member(self.loc, indent+1)}'
		s += f'\n	* rot = {fmt_member(self.rot, indent+1)}'
		s += f'\n	* u_2 = {fmt_member(self.u_2, indent+1)}'
		s += f'\n	* u_3 = {fmt_member(self.u_3, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
