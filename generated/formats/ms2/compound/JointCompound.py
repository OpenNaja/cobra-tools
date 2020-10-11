import typing


class JointCompound:

	"""
	appears in dinos and static meshes
	"""
	namespace_length: int

	# 0s

	# 0s
	zeros: typing.List[int]

	# 1
	unknown_4: int

	# 0
	unknown_5: int

	# 1
	unknown_6: int

	# 0
	unknown_7: int

	# matches bone count from bone info
	bone_count: int

	# 0
	joint_entry_count: int

	# usually 0s
	zeros_1: typing.List[int]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.namespace_length = 0
		self.zeros = []
		self.zeros = []
		self.unknown_4 = 0
		self.unknown_5 = 0
		self.unknown_6 = 0
		self.unknown_7 = 0
		self.bone_count = 0
		self.joint_entry_count = 0
		self.zeros_1 = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.namespace_length = stream.read_uint()
		if not (stream.version == 18):
			self.zeros = [stream.read_uint() for _ in range(13)]
		if stream.version == 18:
			self.zeros = [stream.read_uint() for _ in range(17)]
		self.unknown_4 = stream.read_uint()
		self.unknown_5 = stream.read_uint()
		self.unknown_6 = stream.read_uint()
		self.unknown_7 = stream.read_uint()
		self.bone_count = stream.read_uint()
		self.joint_entry_count = stream.read_uint()
		self.zeros_1 = [stream.read_uint() for _ in range(4)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.namespace_length)
		if not (stream.version == 18):
			for item in self.zeros: stream.write_uint(item)
		if stream.version == 18:
			for item in self.zeros: stream.write_uint(item)
		stream.write_uint(self.unknown_4)
		stream.write_uint(self.unknown_5)
		stream.write_uint(self.unknown_6)
		stream.write_uint(self.unknown_7)
		stream.write_uint(self.bone_count)
		stream.write_uint(self.joint_entry_count)
		for item in self.zeros_1: stream.write_uint(item)

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
