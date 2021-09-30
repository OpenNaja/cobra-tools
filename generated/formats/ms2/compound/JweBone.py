from generated.context import ContextReference
from generated.formats.ms2.compound.Vector3 import Vector3
from generated.formats.ms2.compound.Vector4 import Vector4


class JweBone:

	"""
	32 bytes
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.loc = Vector3(context, None, None)
		self.scale = 0
		self.rot = Vector4(context, None, None)

	def read(self, stream):

		self.io_start = stream.tell()
		self.loc = stream.read_type(Vector3, (self.context, None, None))
		self.scale = stream.read_float()
		self.rot = stream.read_type(Vector4, (self.context, None, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.loc)
		stream.write_float(self.scale)
		stream.write_type(self.rot)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'JweBone [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* loc = {self.loc.__repr__()}'
		s += f'\n	* scale = {self.scale.__repr__()}'
		s += f'\n	* rot = {self.rot.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s

	def set_bone(self, matrix):
		pos, quat, sca = matrix.decompose()
		self.loc.x, self.loc.y, self.loc.z = pos.x, pos.y, pos.z
		self.rot.x, self.rot.y, self.rot.z, self.rot.w = quat.x, quat.y, quat.z, quat.w
		self.scale = sca.x

