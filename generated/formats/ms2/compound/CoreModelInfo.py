import typing
from generated.formats.ms2.compound.Vector3 import Vector3


class CoreModelInfo:

	"""
	Used by ms2 or in Mdl2ModelInfo
	In load order it always defines the variable fragments for the next mdl2
	The mdl2's fragment informs the first mdl2
	"""
	unk_vec_a: Vector3
	unk_float_a: float
	unk_vec_b: Vector3

	# scale: pack_offset / 512, also added as offset
	pack_offset: float

	# always?
	zero_a: float
	unk_float_b: float
	unknownvectors: typing.List[Vector3]
	unk_float_0: float
	unk_float_1: float

	# PZ only
	unk_vec_a_repeat: Vector3

	# PZ only
	unk_vec_b_repeat: Vector3
	mat_count: int
	lod_count: int
	mat_1_count: int

	# count of modeldata fragments for the mdl2 this struct refers to
	model_count: int
	last_count: int
	unk_0: int
	unk_1: int
	pad: typing.List[int]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.unk_vec_a = Vector3()
		self.unk_float_a = 0
		self.unk_vec_b = Vector3()
		self.pack_offset = 0
		self.zero_a = 0
		self.unk_float_b = 0
		self.unknownvectors = []
		self.unk_float_0 = 0
		self.unk_float_1 = 0
		self.unk_vec_a_repeat = Vector3()
		self.unk_vec_b_repeat = Vector3()
		self.mat_count = 0
		self.lod_count = 0
		self.mat_1_count = 0
		self.model_count = 0
		self.last_count = 0
		self.unk_0 = 0
		self.unk_1 = 0
		self.pad = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.unk_vec_a = stream.read_type(Vector3)
		self.unk_float_a = stream.read_float()
		self.unk_vec_b = stream.read_type(Vector3)
		self.pack_offset = stream.read_float()
		self.zero_a = stream.read_float()
		self.unk_float_b = stream.read_float()
		self.unknownvectors = [stream.read_type(Vector3) for _ in range(2)]
		if (stream.user_version == 24724) and (stream.version == 19):
			self.unk_float_0 = stream.read_float()
			self.unk_float_1 = stream.read_float()
		if (stream.user_version == 8340) and (stream.version == 19):
			self.unk_vec_a_repeat = stream.read_type(Vector3)
			self.unk_vec_b_repeat = stream.read_type(Vector3)
		self.mat_count = stream.read_ushort()
		self.lod_count = stream.read_ushort()
		self.mat_1_count = stream.read_ushort()
		self.model_count = stream.read_ushort()
		self.last_count = stream.read_ushort()
		self.unk_0 = stream.read_uint64()
		self.unk_1 = stream.read_uint64()
		self.pad = [stream.read_ubyte() for _ in range(6)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.unk_vec_a)
		stream.write_float(self.unk_float_a)
		stream.write_type(self.unk_vec_b)
		stream.write_float(self.pack_offset)
		stream.write_float(self.zero_a)
		stream.write_float(self.unk_float_b)
		for item in self.unknownvectors: stream.write_type(item)
		if (stream.user_version == 24724) and (stream.version == 19):
			stream.write_float(self.unk_float_0)
			stream.write_float(self.unk_float_1)
		if (stream.user_version == 8340) and (stream.version == 19):
			stream.write_type(self.unk_vec_a_repeat)
			stream.write_type(self.unk_vec_b_repeat)
		stream.write_ushort(self.mat_count)
		stream.write_ushort(self.lod_count)
		stream.write_ushort(self.mat_1_count)
		stream.write_ushort(self.model_count)
		stream.write_ushort(self.last_count)
		stream.write_uint64(self.unk_0)
		stream.write_uint64(self.unk_1)
		for item in self.pad: stream.write_ubyte(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'CoreModelInfo [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* unk_vec_a = ' + self.unk_vec_a.__repr__()
		s += '\n	* unk_float_a = ' + self.unk_float_a.__repr__()
		s += '\n	* unk_vec_b = ' + self.unk_vec_b.__repr__()
		s += '\n	* pack_offset = ' + self.pack_offset.__repr__()
		s += '\n	* zero_a = ' + self.zero_a.__repr__()
		s += '\n	* unk_float_b = ' + self.unk_float_b.__repr__()
		s += '\n	* unknownvectors = ' + self.unknownvectors.__repr__()
		s += '\n	* unk_float_0 = ' + self.unk_float_0.__repr__()
		s += '\n	* unk_float_1 = ' + self.unk_float_1.__repr__()
		s += '\n	* unk_vec_a_repeat = ' + self.unk_vec_a_repeat.__repr__()
		s += '\n	* unk_vec_b_repeat = ' + self.unk_vec_b_repeat.__repr__()
		s += '\n	* mat_count = ' + self.mat_count.__repr__()
		s += '\n	* lod_count = ' + self.lod_count.__repr__()
		s += '\n	* mat_1_count = ' + self.mat_1_count.__repr__()
		s += '\n	* model_count = ' + self.model_count.__repr__()
		s += '\n	* last_count = ' + self.last_count.__repr__()
		s += '\n	* unk_0 = ' + self.unk_0.__repr__()
		s += '\n	* unk_1 = ' + self.unk_1.__repr__()
		s += '\n	* pad = ' + self.pad.__repr__()
		s += '\n'
		return s
