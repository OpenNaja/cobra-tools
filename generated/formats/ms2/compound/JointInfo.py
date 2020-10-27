import typing
from generated.array import Array
from generated.formats.ms2.compound.HitCheckEntry import HitCheckEntry


class JointInfo:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# must be 11
		self.eleven = 0

		# bunch of -1's
		self.f_fs = Array()
		self.name_offset = 0
		self.hitcheck_count = 0

		# 8 bytes of zeros
		self.zero = 0

		# 8 bytes of zeros per hitcheck
		self.zeros_per_hitcheck = Array()
		self.hit_check = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.eleven = stream.read_uint()
		self.f_fs.read(stream, 'Short', 6, None)
		self.name_offset = stream.read_uint()
		self.hitcheck_count = stream.read_uint()
		self.zero = stream.read_uint64()
		self.zeros_per_hitcheck.read(stream, 'Uint64', self.hitcheck_count, None)
		self.hit_check.read(stream, HitCheckEntry, self.hitcheck_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.eleven)
		self.f_fs.write(stream, 'Short', 6, None)
		stream.write_uint(self.name_offset)
		stream.write_uint(self.hitcheck_count)
		stream.write_uint64(self.zero)
		self.zeros_per_hitcheck.write(stream, 'Uint64', self.hitcheck_count, None)
		self.hit_check.write(stream, HitCheckEntry, self.hitcheck_count, None)

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
