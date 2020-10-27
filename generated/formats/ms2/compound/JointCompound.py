import typing
from generated.array import Array


class JointCompound:

	"""
	appears in dinos and static meshes
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.namespace_length = 0

		# 0s
		self.zeros = Array()

		# 0s
		self.zeros = Array()

		# 1
		self.unknown_4 = 0

		# 0
		self.unknown_5 = 0

		# 1
		self.unknown_6 = 0

		# 0
		self.unknown_7 = 0

		# matches bone count from bone info
		self.bone_count = 0

		# 0
		self.joint_entry_count = 0

		# usually 0s
		self.zeros_1 = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.namespace_length = stream.read_uint()
		if not (stream.version == 18):
			self.zeros.read(stream, 'Uint', 13, None)
		if stream.version == 18:
			self.zeros.read(stream, 'Uint', 17, None)
		self.unknown_4 = stream.read_uint()
		self.unknown_5 = stream.read_uint()
		self.unknown_6 = stream.read_uint()
		self.unknown_7 = stream.read_uint()
		self.bone_count = stream.read_uint()
		self.joint_entry_count = stream.read_uint()
		self.zeros_1.read(stream, 'Uint', 4, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.namespace_length)
		if not (stream.version == 18):
			self.zeros.write(stream, 'Uint', 13, None)
		if stream.version == 18:
			self.zeros.write(stream, 'Uint', 17, None)
		stream.write_uint(self.unknown_4)
		stream.write_uint(self.unknown_5)
		stream.write_uint(self.unknown_6)
		stream.write_uint(self.unknown_7)
		stream.write_uint(self.bone_count)
		stream.write_uint(self.joint_entry_count)
		self.zeros_1.write(stream, 'Uint', 4, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'JointCompound [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* namespace_length = ' + self.namespace_length.__repr__()
		s += '\n	* zeros = ' + self.zeros.__repr__()
		s += '\n	* unknown_4 = ' + self.unknown_4.__repr__()
		s += '\n	* unknown_5 = ' + self.unknown_5.__repr__()
		s += '\n	* unknown_6 = ' + self.unknown_6.__repr__()
		s += '\n	* unknown_7 = ' + self.unknown_7.__repr__()
		s += '\n	* bone_count = ' + self.bone_count.__repr__()
		s += '\n	* joint_entry_count = ' + self.joint_entry_count.__repr__()
		s += '\n	* zeros_1 = ' + self.zeros_1.__repr__()
		s += '\n'
		return s
