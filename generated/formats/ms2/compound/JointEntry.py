from generated.context import ContextReference
from generated.formats.ms2.compound.Matrix33 import Matrix33
from generated.formats.ms2.compound.Vector3 import Vector3


class JointEntry:

	"""
	Describes a joint in armature space.
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# the rotation of the joint, inverted
		self.rot = Matrix33(context, None, None)

		# the location of the joint
		self.loc = Vector3(context, None, None)

	def read(self, stream):

		self.io_start = stream.tell()
		self.rot = stream.read_type(Matrix33)
		self.loc = stream.read_type(Vector3)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.rot)
		stream.write_type(self.loc)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'JointEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* rot = {self.rot.__repr__()}'
		s += f'\n	* loc = {self.loc.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
