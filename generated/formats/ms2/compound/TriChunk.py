from generated.formats.base.basic import fmt_member
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.ms2.compound.QuatWFirst import QuatWFirst
from generated.formats.ms2.compound.Vector3 import Vector3
from generated.struct import StructBase


class TriChunk(StructBase):

	"""
	JWE2 Biosyn: 64 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# the smallest coordinates across all axes, min of unpacked vert coords if loc is 0,0,0
		self.bounds_min = 0
		self.u_0 = 0
		self.u_1 = 0

		# the biggest coordinates across all axes, max of unpacked vert coords if loc is 0,0,0
		self.bounds_max = 0
		self.tris_offset = 0

		# can be 0,0,0, no obvious range, not always within range of bounds
		self.loc = 0

		# can be 1, 0, 0, 0; w always in range -1, +1
		self.rot = 0
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
		self.rot = QuatWFirst(self.context, 0, None)
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
		super().read_fields(stream, instance)
		instance.bounds_min = Vector3.from_stream(stream, instance.context, 0, None)
		instance.u_0 = stream.read_ushort()
		instance.u_1 = stream.read_ushort()
		instance.bounds_max = Vector3.from_stream(stream, instance.context, 0, None)
		instance.tris_offset = stream.read_uint()
		instance.loc = Vector3.from_stream(stream, instance.context, 0, None)
		instance.rot = QuatWFirst.from_stream(stream, instance.context, 0, None)
		instance.u_2 = stream.read_ushort()
		instance.u_3 = stream.read_ushort()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Vector3.to_stream(stream, instance.bounds_min)
		stream.write_ushort(instance.u_0)
		stream.write_ushort(instance.u_1)
		Vector3.to_stream(stream, instance.bounds_max)
		stream.write_uint(instance.tris_offset)
		Vector3.to_stream(stream, instance.loc)
		QuatWFirst.to_stream(stream, instance.rot)
		stream.write_ushort(instance.u_2)
		stream.write_ushort(instance.u_3)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('bounds_min', Vector3, (0, None))
		yield ('u_0', Ushort, (0, None))
		yield ('u_1', Ushort, (0, None))
		yield ('bounds_max', Vector3, (0, None))
		yield ('tris_offset', Uint, (0, None))
		yield ('loc', Vector3, (0, None))
		yield ('rot', QuatWFirst, (0, None))
		yield ('u_2', Ushort, (0, None))
		yield ('u_3', Ushort, (0, None))

	def get_info_str(self, indent=0):
		return f'TriChunk [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
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
