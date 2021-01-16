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
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# the smallest coordinates across all axes
		self.bounds_min = Vector3()
		self.unk_float_a = 0

		# the biggest coordinates across all axes
		self.bounds_max = Vector3()

		# scale: pack_offset / 512, also added as offset
		self.pack_offset = 0

		# cog? medium of bounds?
		self.center = Vector3()

		# probably from center to max
		self.radius = 0

		# PZ only, zero-ish
		self.unknowns = Array()
		self.bounds_min_repeat = Vector3()
		self.bounds_max_repeat = Vector3()
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
		self.bounds_min = stream.read_type(Vector3)
		self.unk_float_a = stream.read_float()
		self.bounds_max = stream.read_type(Vector3)
		self.pack_offset = stream.read_float()
		self.center = stream.read_type(Vector3)
		self.radius = stream.read_float()
		if ((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version == 19):
			self.unknowns = stream.read_floats((4))
		self.bounds_min_repeat = stream.read_type(Vector3)
		self.bounds_max_repeat = stream.read_type(Vector3)
		self.mat_count = stream.read_ushort()
		self.lod_count = stream.read_ushort()
		self.mat_1_count = stream.read_ushort()
		self.model_count = stream.read_ushort()
		self.last_count = stream.read_ushort()
		self.unk_0 = stream.read_uint64()
		self.unk_1 = stream.read_uint64()
		self.pad = stream.read_ubytes((6))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.bounds_min)
		stream.write_float(self.unk_float_a)
		stream.write_type(self.bounds_max)
		stream.write_float(self.pack_offset)
		stream.write_type(self.center)
		stream.write_float(self.radius)
		if ((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version == 19):
			stream.write_floats(self.unknowns)
		stream.write_type(self.bounds_min_repeat)
		stream.write_type(self.bounds_max_repeat)
		stream.write_ushort(self.mat_count)
		stream.write_ushort(self.lod_count)
		stream.write_ushort(self.mat_1_count)
		stream.write_ushort(self.model_count)
		stream.write_ushort(self.last_count)
		stream.write_uint64(self.unk_0)
		stream.write_uint64(self.unk_1)
		stream.write_ubytes(self.pad)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'CoreModelInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* bounds_min = {self.bounds_min.__repr__()}'
		s += f'\n	* unk_float_a = {self.unk_float_a.__repr__()}'
		s += f'\n	* bounds_max = {self.bounds_max.__repr__()}'
		s += f'\n	* pack_offset = {self.pack_offset.__repr__()}'
		s += f'\n	* center = {self.center.__repr__()}'
		s += f'\n	* radius = {self.radius.__repr__()}'
		s += f'\n	* unknowns = {self.unknowns.__repr__()}'
		s += f'\n	* bounds_min_repeat = {self.bounds_min_repeat.__repr__()}'
		s += f'\n	* bounds_max_repeat = {self.bounds_max_repeat.__repr__()}'
		s += f'\n	* mat_count = {self.mat_count.__repr__()}'
		s += f'\n	* lod_count = {self.lod_count.__repr__()}'
		s += f'\n	* mat_1_count = {self.mat_1_count.__repr__()}'
		s += f'\n	* model_count = {self.model_count.__repr__()}'
		s += f'\n	* last_count = {self.last_count.__repr__()}'
		s += f'\n	* unk_0 = {self.unk_0.__repr__()}'
		s += f'\n	* unk_1 = {self.unk_1.__repr__()}'
		s += f'\n	* pad = {self.pad.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
