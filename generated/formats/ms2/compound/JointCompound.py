import typing
from generated.array import Array


class JointCompound:

	"""
	appears in dinos and static meshes
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# repeat
		self.joint_count = 0

		# small number
		self.count_0 = 0

		# small number
		self.count_1 = 0

		# small number
		self.count_2 = 0
		self.namespace_length = 0

		# 0s
		self.zeros = Array()

		# 0s
		self.zeros = Array()

		# 1, 1
		self.ones = Array()

		# matches bone count from bone info
		self.bone_count = 0

		# 0
		self.joint_entry_count = 0

		# usually 0s
		self.zeros_1 = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.joint_count = stream.read_uint()
		self.count_0 = stream.read_uint()
		self.count_1 = stream.read_uint()
		self.count_2 = stream.read_uint()
		self.namespace_length = stream.read_uint()
		if not (stream.version == 18):
			self.zeros = stream.read_uints((13))
		if stream.version == 18:
			self.zeros = stream.read_uints((17))
		self.ones = stream.read_uint64s((2))
		self.bone_count = stream.read_uint()
		self.joint_entry_count = stream.read_uint()
		self.zeros_1 = stream.read_uints((4))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.joint_count)
		stream.write_uint(self.count_0)
		stream.write_uint(self.count_1)
		stream.write_uint(self.count_2)
		stream.write_uint(self.namespace_length)
		if not (stream.version == 18):
			stream.write_uints(self.zeros)
		if stream.version == 18:
			stream.write_uints(self.zeros)
		stream.write_uint64s(self.ones)
		stream.write_uint(self.bone_count)
		stream.write_uint(self.joint_entry_count)
		stream.write_uints(self.zeros_1)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'JointCompound [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* joint_count = {self.joint_count.__repr__()}'
		s += f'\n	* count_0 = {self.count_0.__repr__()}'
		s += f'\n	* count_1 = {self.count_1.__repr__()}'
		s += f'\n	* count_2 = {self.count_2.__repr__()}'
		s += f'\n	* namespace_length = {self.namespace_length.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* ones = {self.ones.__repr__()}'
		s += f'\n	* bone_count = {self.bone_count.__repr__()}'
		s += f'\n	* joint_entry_count = {self.joint_entry_count.__repr__()}'
		s += f'\n	* zeros_1 = {self.zeros_1.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
