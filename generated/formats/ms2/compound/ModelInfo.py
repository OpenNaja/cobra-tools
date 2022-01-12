import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.bitfield.RenderFlag import RenderFlag
from generated.formats.ms2.compound.Vector3 import Vector3


class ModelInfo:

	"""
	Linked to by the ms2, part of an array
	120 bytes for JWE2
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# the smallest coordinates across all axes
		self.bounds_min = Vector3(self.context, None, None)

		# not sure, for PZ often 40 00 00 37 for animals
		self.unk_float_a = 0

		# the biggest coordinates across all axes
		self.bounds_max = Vector3(self.context, None, None)

		# scale: pack_offset / 512, also added as offset
		self.pack_offset = 0

		# cog? medium of bounds?
		self.center = Vector3(self.context, None, None)

		# probably from center to max
		self.radius = 0

		# seen 6 or 1, matches lod count
		self.num_lods_2 = 0

		# zero
		self.zero = 0

		# verbatim repeat
		self.bounds_min_repeat = Vector3(self.context, None, None)

		# verbatim repeat
		self.bounds_max_repeat = Vector3(self.context, None, None)
		self.num_materials = 0
		self.num_lods = 0
		self.num_objects = 0

		# count of MeshData fragments for the mdl2 this struct refers to
		self.num_meshes = 0

		# ?
		self.last_count = 0

		# this has influence on whether newly added shells draw correctly; for PZ usually 4, except for furry animals; ZT african ele female
		self.render_flag = RenderFlag()

		# ?
		self.unks = numpy.zeros((7), dtype='ushort')
		self.pad = numpy.zeros((3), dtype='ushort')
		self.materials_ptr = 0
		self.lods_ptr = 0
		self.objects_ptr = 0
		self.models_ptr = 0
		self.first_materials_ptr = 0
		self.zeros_ztuac = numpy.zeros((3), dtype='uint64')

		# unknown, probably used to increment skeleton
		self.increment_flag = 0
		self.zero_0 = 0
		self.zero_1 = 0
		self.zero_2 = 0
		self.set_defaults()

	def set_defaults(self):
		self.bounds_min = Vector3(self.context, None, None)
		if not (self.context.version < 19):
			self.unk_float_a = 0
		self.bounds_max = Vector3(self.context, None, None)
		if not (self.context.version < 19):
			self.pack_offset = 0
		self.center = Vector3(self.context, None, None)
		self.radius = 0
		if ((not self.context.user_version.is_jwe) and (self.context.version >= 19)) or (self.context.user_version.is_jwe and (self.context.version == 20)):
			self.num_lods_2 = 0
		if ((not self.context.user_version.is_jwe) and (self.context.version >= 19)) or (self.context.user_version.is_jwe and (self.context.version == 20)):
			self.zero = 0
		if not (self.context.version == 17):
			self.bounds_min_repeat = Vector3(self.context, None, None)
		if not (self.context.version == 17):
			self.bounds_max_repeat = Vector3(self.context, None, None)
		self.num_materials = 0
		self.num_lods = 0
		self.num_objects = 0
		self.num_meshes = 0
		self.last_count = 0
		self.render_flag = RenderFlag()
		self.unks = numpy.zeros((7), dtype='ushort')
		self.pad = numpy.zeros((3), dtype='ushort')
		self.materials_ptr = 0
		self.lods_ptr = 0
		self.objects_ptr = 0
		self.models_ptr = 0
		self.first_materials_ptr = 0
		if self.context.version == 17:
			self.zeros_ztuac = numpy.zeros((3), dtype='uint64')
		self.increment_flag = 0
		self.zero_0 = 0
		if not (self.context.version == 18):
			self.zero_1 = 0
		if not (self.context.version < 19):
			self.zero_2 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.bounds_min = stream.read_type(Vector3, (self.context, None, None))
		if not (self.context.version < 19):
			self.unk_float_a = stream.read_float()
		self.bounds_max = stream.read_type(Vector3, (self.context, None, None))
		if not (self.context.version < 19):
			self.pack_offset = stream.read_float()
		self.center = stream.read_type(Vector3, (self.context, None, None))
		self.radius = stream.read_float()
		if ((not self.context.user_version.is_jwe) and (self.context.version >= 19)) or (self.context.user_version.is_jwe and (self.context.version == 20)):
			self.num_lods_2 = stream.read_uint64()
			self.zero = stream.read_uint64()
		if not (self.context.version == 17):
			self.bounds_min_repeat = stream.read_type(Vector3, (self.context, None, None))
			self.bounds_max_repeat = stream.read_type(Vector3, (self.context, None, None))
		self.num_materials = stream.read_ushort()
		self.num_lods = stream.read_ushort()
		self.num_objects = stream.read_ushort()
		self.num_meshes = stream.read_ushort()
		self.last_count = stream.read_ushort()
		self.render_flag = stream.read_type(RenderFlag)
		self.unks = stream.read_ushorts((7))
		self.pad = stream.read_ushorts((3))
		self.materials_ptr = stream.read_uint64()
		self.lods_ptr = stream.read_uint64()
		self.objects_ptr = stream.read_uint64()
		self.models_ptr = stream.read_uint64()
		self.first_materials_ptr = stream.read_uint64()
		if self.context.version == 17:
			self.zeros_ztuac = stream.read_uint64s((3))
		self.increment_flag = stream.read_uint64()
		self.zero_0 = stream.read_uint64()
		if not (self.context.version == 18):
			self.zero_1 = stream.read_uint64()
		if not (self.context.version < 19):
			self.zero_2 = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.bounds_min)
		if not (self.context.version < 19):
			stream.write_float(self.unk_float_a)
		stream.write_type(self.bounds_max)
		if not (self.context.version < 19):
			stream.write_float(self.pack_offset)
		stream.write_type(self.center)
		stream.write_float(self.radius)
		if ((not self.context.user_version.is_jwe) and (self.context.version >= 19)) or (self.context.user_version.is_jwe and (self.context.version == 20)):
			stream.write_uint64(self.num_lods_2)
			stream.write_uint64(self.zero)
		if not (self.context.version == 17):
			stream.write_type(self.bounds_min_repeat)
			stream.write_type(self.bounds_max_repeat)
		stream.write_ushort(self.num_materials)
		stream.write_ushort(self.num_lods)
		stream.write_ushort(self.num_objects)
		stream.write_ushort(self.num_meshes)
		stream.write_ushort(self.last_count)
		stream.write_type(self.render_flag)
		stream.write_ushorts(self.unks)
		stream.write_ushorts(self.pad)
		stream.write_uint64(self.materials_ptr)
		stream.write_uint64(self.lods_ptr)
		stream.write_uint64(self.objects_ptr)
		stream.write_uint64(self.models_ptr)
		stream.write_uint64(self.first_materials_ptr)
		if self.context.version == 17:
			stream.write_uint64s(self.zeros_ztuac)
		stream.write_uint64(self.increment_flag)
		stream.write_uint64(self.zero_0)
		if not (self.context.version == 18):
			stream.write_uint64(self.zero_1)
		if not (self.context.version < 19):
			stream.write_uint64(self.zero_2)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ModelInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* bounds_min = {self.bounds_min.__repr__()}'
		s += f'\n	* unk_float_a = {self.unk_float_a.__repr__()}'
		s += f'\n	* bounds_max = {self.bounds_max.__repr__()}'
		s += f'\n	* pack_offset = {self.pack_offset.__repr__()}'
		s += f'\n	* center = {self.center.__repr__()}'
		s += f'\n	* radius = {self.radius.__repr__()}'
		s += f'\n	* num_lods_2 = {self.num_lods_2.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		s += f'\n	* bounds_min_repeat = {self.bounds_min_repeat.__repr__()}'
		s += f'\n	* bounds_max_repeat = {self.bounds_max_repeat.__repr__()}'
		s += f'\n	* num_materials = {self.num_materials.__repr__()}'
		s += f'\n	* num_lods = {self.num_lods.__repr__()}'
		s += f'\n	* num_objects = {self.num_objects.__repr__()}'
		s += f'\n	* num_meshes = {self.num_meshes.__repr__()}'
		s += f'\n	* last_count = {self.last_count.__repr__()}'
		s += f'\n	* render_flag = {self.render_flag.__repr__()}'
		s += f'\n	* unks = {self.unks.__repr__()}'
		s += f'\n	* pad = {self.pad.__repr__()}'
		s += f'\n	* materials_ptr = {self.materials_ptr.__repr__()}'
		s += f'\n	* lods_ptr = {self.lods_ptr.__repr__()}'
		s += f'\n	* objects_ptr = {self.objects_ptr.__repr__()}'
		s += f'\n	* models_ptr = {self.models_ptr.__repr__()}'
		s += f'\n	* first_materials_ptr = {self.first_materials_ptr.__repr__()}'
		s += f'\n	* zeros_ztuac = {self.zeros_ztuac.__repr__()}'
		s += f'\n	* increment_flag = {self.increment_flag.__repr__()}'
		s += f'\n	* zero_0 = {self.zero_0.__repr__()}'
		s += f'\n	* zero_1 = {self.zero_1.__repr__()}'
		s += f'\n	* zero_2 = {self.zero_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
