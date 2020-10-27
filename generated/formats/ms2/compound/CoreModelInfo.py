import typing
from generated.array import Array
from generated.formats.ms2.compound.Vector3 import Vector3


class CoreModelInfo:

	"""
	Used by ms2 or in Mdl2ModelInfo
	In load order it always defines the variable fragments for the next mdl2
	The mdl2's fragment informs the first mdl2
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.unk_vec_a = Vector3()
		self.unk_float_a = 0
		self.unk_vec_b = Vector3()

		# scale: pack_offset / 512, also added as offset
		self.pack_offset = 0

		# always?
		self.zero_a = 0
		self.unk_float_b = 0
		self.unknownvectors = Array()
		self.unk_float_0 = 0
		self.unk_float_1 = 0

		# PZ only
		self.unk_vec_a_repeat = Vector3()

		# PZ only
		self.unk_vec_b_repeat = Vector3()
		self.mat_count = 0
		self.lod_count = 0
		self.mat_1_count = 0

		# count of modeldata fragments for the mdl2 this struct refers to
		self.model_count = 0
		self.last_count = 0
		self.unk_0 = 0
		self.unk_1 = 0
		self.pad = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.unk_vec_a = stream.read_type(Vector3)
		self.unk_float_a = stream.read_float()
		self.unk_vec_b = stream.read_type(Vector3)
		self.pack_offset = stream.read_float()
		self.zero_a = stream.read_float()
		self.unk_float_b = stream.read_float()
		self.unknownvectors.read(stream, Vector3, 2, None)
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
		self.pad.read(stream, 'Ubyte', 6, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.unk_vec_a)
		stream.write_float(self.unk_float_a)
		stream.write_type(self.unk_vec_b)
		stream.write_float(self.pack_offset)
		stream.write_float(self.zero_a)
		stream.write_float(self.unk_float_b)
		self.unknownvectors.write(stream, Vector3, 2, None)
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
		self.pad.write(stream, 'Ubyte', 6, None)

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
