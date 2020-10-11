from generated.formats.ms2.compound.Vector3 import Vector3
from generated.formats.ms2.compound.Vector4 import Vector4


class JweBone:

	"""
	32 bytes
	"""
	loc: Vector3
	scale: float
	rot: Vector4

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.loc = Vector3()
		self.scale = 0
		self.rot = Vector4()

	def read(self, stream):

		self.io_start = stream.tell()
		self.loc = stream.read_type(Vector3)
		self.scale = stream.read_float()
		self.rot = stream.read_type(Vector4)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.loc)
		stream.write_float(self.scale)
		stream.write_type(self.rot)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'JweBone [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* loc = ' + self.loc.__repr__()
		s += '\n	* scale = ' + self.scale.__repr__()
		s += '\n	* rot = ' + self.rot.__repr__()
		s += '\n'
		return s

	def set_bone(self, matrix):
		pos, quat, sca = matrix.decompose()
		self.loc.x, self.loc.y, self.loc.z = -1 * pos.y, pos.z, pos.x
		self.rot.x, self.rot.y, self.rot.z, self.rot.w = quat.y, -1 * quat.z, -1 * quat.x, quat.w
		self.scale = sca.x

