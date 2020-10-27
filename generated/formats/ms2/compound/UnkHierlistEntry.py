class UnkHierlistEntry:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.bone_index_1 = 0

		# dunno what these do at the moment
		self.bone_index_2 = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.bone_index_1 = stream.read_uint()
		self.bone_index_2 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.bone_index_1)
		stream.write_uint(self.bone_index_2)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'UnkHierlistEntry [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* bone_index_1 = ' + self.bone_index_1.__repr__()
		s += '\n	* bone_index_2 = ' + self.bone_index_2.__repr__()
		s += '\n'
		return s
