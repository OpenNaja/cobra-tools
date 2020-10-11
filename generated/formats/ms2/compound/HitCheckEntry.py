from generated.formats.ms2.compound.BoundingBox import BoundingBox
from generated.formats.ms2.compound.Capsule import Capsule


class HitCheckEntry:
	type: int
	unknown_2_a: int
	unknown_2_b: int

	# 16
	unknown_2_c: int

	# 0
	unknown_2_d: int

	# 564267
	unknown_3: int

	# 46
	unknown_4: int
	namespace_offset: int
	bbox: BoundingBox
	capsule: Capsule

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.type = 0
		self.unknown_2_a = 0
		self.unknown_2_b = 0
		self.unknown_2_c = 0
		self.unknown_2_d = 0
		self.unknown_3 = 0
		self.unknown_4 = 0
		self.namespace_offset = 0
		self.bbox = BoundingBox()
		self.capsule = Capsule()

	def read(self, stream):

		self.io_start = stream.tell()
		self.type = stream.read_uint()
		self.unknown_2_a = stream.read_ubyte()
		self.unknown_2_b = stream.read_ubyte()
		self.unknown_2_c = stream.read_ubyte()
		self.unknown_2_d = stream.read_ubyte()
		self.unknown_3 = stream.read_uint()
		self.unknown_4 = stream.read_uint()
		self.namespace_offset = stream.read_uint()
		if self.type == 1:
			self.bbox = stream.read_type(BoundingBox)
		if self.type == 2:
			self.capsule = stream.read_type(Capsule)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.type)
		stream.write_ubyte(self.unknown_2_a)
		stream.write_ubyte(self.unknown_2_b)
		stream.write_ubyte(self.unknown_2_c)
		stream.write_ubyte(self.unknown_2_d)
		stream.write_uint(self.unknown_3)
		stream.write_uint(self.unknown_4)
		stream.write_uint(self.namespace_offset)
		if self.type == 1:
			stream.write_type(self.bbox)
		if self.type == 2:
			stream.write_type(self.capsule)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'HitCheckEntry [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* type = ' + self.type.__repr__()
		s += '\n	* unknown_2_a = ' + self.unknown_2_a.__repr__()
		s += '\n	* unknown_2_b = ' + self.unknown_2_b.__repr__()
		s += '\n	* unknown_2_c = ' + self.unknown_2_c.__repr__()
		s += '\n	* unknown_2_d = ' + self.unknown_2_d.__repr__()
		s += '\n	* unknown_3 = ' + self.unknown_3.__repr__()
		s += '\n	* unknown_4 = ' + self.unknown_4.__repr__()
		s += '\n	* namespace_offset = ' + self.namespace_offset.__repr__()
		s += '\n	* bbox = ' + self.bbox.__repr__()
		s += '\n	* capsule = ' + self.capsule.__repr__()
		s += '\n'
		return s
