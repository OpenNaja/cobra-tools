import typing
from generated.formats.ms2.compound.HitCheckEntry import HitCheckEntry


class JointInfo:

	# must be 11
	eleven: int

	# bunch of -1's
	f_fs: typing.List[int]
	name_offset: int
	hitcheck_count: int

	# 8 bytes of zeros
	zero: int

	# 8 bytes of zeros per hitcheck
	zeros_per_hitcheck: typing.List[int]
	hit_check: typing.List[HitCheckEntry]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.eleven = 0
		self.f_fs = []
		self.name_offset = 0
		self.hitcheck_count = 0
		self.zero = 0
		self.zeros_per_hitcheck = []
		self.hit_check = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.eleven = stream.read_uint()
		self.f_fs = [stream.read_short() for _ in range(6)]
		self.name_offset = stream.read_uint()
		self.hitcheck_count = stream.read_uint()
		self.zero = stream.read_uint64()
		self.zeros_per_hitcheck = [stream.read_uint64() for _ in range(self.hitcheck_count)]
		self.hit_check = [stream.read_type(HitCheckEntry) for _ in range(self.hitcheck_count)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.eleven)
		for item in self.f_fs: stream.write_short(item)
		stream.write_uint(self.name_offset)
		stream.write_uint(self.hitcheck_count)
		stream.write_uint64(self.zero)
		for item in self.zeros_per_hitcheck: stream.write_uint64(item)
		for item in self.hit_check: stream.write_type(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'JointInfo [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* eleven = ' + self.eleven.__repr__()
		s += '\n	* f_fs = ' + self.f_fs.__repr__()
		s += '\n	* name_offset = ' + self.name_offset.__repr__()
		s += '\n	* hitcheck_count = ' + self.hitcheck_count.__repr__()
		s += '\n	* zero = ' + self.zero.__repr__()
		s += '\n	* zeros_per_hitcheck = ' + self.zeros_per_hitcheck.__repr__()
		s += '\n	* hit_check = ' + self.hit_check.__repr__()
		s += '\n'
		return s
