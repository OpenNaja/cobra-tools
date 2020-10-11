import typing


class Ms2BufferInfo:

	"""
	Fragment data describing a MS2 buffer giving the size of the whole vertex and tri buffer.
	JWE: 48 bytes
	PZ: 56 bytes
	"""

	# JWE, 16 bytes of 00 padding
	skip_1: typing.List[int]
	vertexdatasize: int

	# 8 empty bytes
	ptr_1: int

	# PZ, another 8 empty bytes
	unk_0: int
	facesdatasize: int

	# 8 empty bytes
	ptr_2: int

	# PZ, another 16 empty bytes
	unk_2: typing.List[int]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.skip_1 = []
		self.vertexdatasize = 0
		self.ptr_1 = 0
		self.unk_0 = 0
		self.facesdatasize = 0
		self.ptr_2 = 0
		self.unk_2 = []

	def read(self, stream):

		self.io_start = stream.tell()
		if (stream.user_version == 24724) and (stream.version == 19):
			self.skip_1 = [stream.read_uint() for _ in range(4)]
		self.vertexdatasize = stream.read_uint64()
		self.ptr_1 = stream.read_uint64()
		if (stream.user_version == 8340) and (stream.version == 19):
			self.unk_0 = stream.read_uint64()
		self.facesdatasize = stream.read_uint64()
		self.ptr_2 = stream.read_uint64()
		if (stream.user_version == 8340) and (stream.version == 19):
			self.unk_2 = [stream.read_uint64() for _ in range(2)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		if (stream.user_version == 24724) and (stream.version == 19):
			for item in self.skip_1: stream.write_uint(item)
		stream.write_uint64(self.vertexdatasize)
		stream.write_uint64(self.ptr_1)
		if (stream.user_version == 8340) and (stream.version == 19):
			stream.write_uint64(self.unk_0)
		stream.write_uint64(self.facesdatasize)
		stream.write_uint64(self.ptr_2)
		if (stream.user_version == 8340) and (stream.version == 19):
			for item in self.unk_2: stream.write_uint64(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Ms2BufferInfo [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* skip_1 = ' + self.skip_1.__repr__()
		s += '\n	* vertexdatasize = ' + self.vertexdatasize.__repr__()
		s += '\n	* ptr_1 = ' + self.ptr_1.__repr__()
		s += '\n	* unk_0 = ' + self.unk_0.__repr__()
		s += '\n	* facesdatasize = ' + self.facesdatasize.__repr__()
		s += '\n	* ptr_2 = ' + self.ptr_2.__repr__()
		s += '\n	* unk_2 = ' + self.unk_2.__repr__()
		s += '\n'
		return s
