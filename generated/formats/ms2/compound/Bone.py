from source.formats.base.basic import fmt_member
from generated.context import ContextReference
from generated.formats.ms2.compound.Vector3 import Vector3
from generated.formats.ms2.compound.Vector4 import Vector4


class Bone:

	"""
	32 bytes
	bones, rot first
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.loc = 0
		self.scale = 0
		self.rot = 0
		self.rot = 0
		self.loc = 0
		self.scale = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if self.context.version <= 47:
			self.loc = Vector3(self.context, 0, None)
			self.scale = 0.0
			self.rot = Vector4(self.context, 0, None)
		if self.context.version >= 48:
			self.rot = Vector4(self.context, 0, None)
			self.loc = Vector3(self.context, 0, None)
			self.scale = 0.0

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
		if instance.context.version <= 47:
			instance.loc = Vector3.from_stream(stream, instance.context, 0, None)
			instance.scale = stream.read_float()
			instance.rot = Vector4.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 48:
			instance.rot = Vector4.from_stream(stream, instance.context, 0, None)
			instance.loc = Vector3.from_stream(stream, instance.context, 0, None)
			instance.scale = stream.read_float()

	@classmethod
	def write_fields(cls, stream, instance):
		if instance.context.version <= 47:
			Vector3.to_stream(stream, instance.loc)
			stream.write_float(instance.scale)
			Vector4.to_stream(stream, instance.rot)
		if instance.context.version >= 48:
			Vector4.to_stream(stream, instance.rot)
			Vector3.to_stream(stream, instance.loc)
			stream.write_float(instance.scale)

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
		return f'Bone [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* loc = {fmt_member(self.loc, indent+1)}'
		s += f'\n	* scale = {fmt_member(self.scale, indent+1)}'
		s += f'\n	* rot = {fmt_member(self.rot, indent+1)}'
		s += f'\n	* loc = {fmt_member(self.loc, indent+1)}'
		s += f'\n	* scale = {fmt_member(self.scale, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s

	def set_bone(self, matrix):
		pos, quat, sca = matrix.decompose()
		self.loc.x, self.loc.y, self.loc.z = pos.x, pos.y, pos.z
		self.rot.x, self.rot.y, self.rot.z, self.rot.w = quat.x, quat.y, quat.z, quat.w
		self.scale = sca.x

