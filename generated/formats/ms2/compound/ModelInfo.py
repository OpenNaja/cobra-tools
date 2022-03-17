import numpy
from generated.context import ContextReference
from generated.formats.ms2.bitfield.RenderFlag import RenderFlag
from generated.formats.ms2.compound.Vector3 import Vector3


class ModelInfo:

	"""
	Linked to by the ms2, part of an array
	120 bytes for JWE2
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# the smallest coordinates across all axes
		self.bounds_min = Vector3(self.context, 0, None)

		# not sure, for PZ often 40 00 00 37 for animals
		self.unk_float_a = 0.0

		# the biggest coordinates across all axes
		self.bounds_max = Vector3(self.context, 0, None)

		# scale: pack_offset / 512, also added as offset
		self.pack_offset = 0.0

		# cog? medium of bounds?
		self.center = Vector3(self.context, 0, None)

		# probably from center to max
		self.radius = 0.0

		# seen 6 or 1, matches lod count
		self.num_lods_2 = 0

		# zero
		self.zero = 0

		# verbatim repeat
		self.bounds_min_repeat = Vector3(self.context, 0, None)

		# verbatim repeat
		self.bounds_max_repeat = Vector3(self.context, 0, None)
		self.num_materials = 0
		self.num_lods = 0
		self.num_objects = 0

		# count of MeshData fragments for the mdl2 this struct refers to
		self.num_meshes = 0

		# ?
		self.last_count = 0

		# this has influence on whether newly added shells draw correctly; for PZ usually 4, except for furry animals; ZT african ele female
		self.render_flag = RenderFlag(self.context, 0, None)

		# ?
		self.unks = numpy.zeros((7,), dtype=numpy.dtype('uint16'))
		self.pad = numpy.zeros((3,), dtype=numpy.dtype('uint16'))
		self.materials_ptr = 0
		self.lods_ptr = 0
		self.objects_ptr = 0
		self.models_ptr = 0
		self.first_materials_ptr = 0
		self.zeros_ztuac = numpy.zeros((4,), dtype=numpy.dtype('uint64'))

		# unknown, probably used to increment skeleton
		self.increment_flag = 0
		self.zero_0 = 0
		self.zero_1 = 0
		self.zero_2 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.bounds_min = Vector3(self.context, 0, None)
		if self.context.version >= 47:
			self.unk_float_a = 0.0
		self.bounds_max = Vector3(self.context, 0, None)
		if self.context.version >= 47:
			self.pack_offset = 0.0
		self.center = Vector3(self.context, 0, None)
		self.radius = 0.0
		if self.context.version >= 48:
			self.num_lods_2 = 0
		if self.context.version >= 48:
			self.zero = 0
		if self.context.version >= 32:
			self.bounds_min_repeat = Vector3(self.context, 0, None)
		if self.context.version >= 32:
			self.bounds_max_repeat = Vector3(self.context, 0, None)
		self.num_materials = 0
		self.num_lods = 0
		self.num_objects = 0
		self.num_meshes = 0
		self.last_count = 0
		self.render_flag = RenderFlag(self.context, 0, None)
		self.unks = numpy.zeros((7,), dtype=numpy.dtype('uint16'))
		self.pad = numpy.zeros((3,), dtype=numpy.dtype('uint16'))
		self.materials_ptr = 0
		self.lods_ptr = 0
		self.objects_ptr = 0
		self.models_ptr = 0
		self.first_materials_ptr = 0
		if self.context.version == 13:
			self.zeros_ztuac = numpy.zeros((4,), dtype=numpy.dtype('uint64'))
		self.increment_flag = 0
		self.zero_0 = 0
		if not (self.context.version == 32):
			self.zero_1 = 0
		if self.context.version >= 47:
			self.zero_2 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		instance.bounds_min = Vector3.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 47:
			instance.unk_float_a = stream.read_float()
		instance.bounds_max = Vector3.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 47:
			instance.pack_offset = stream.read_float()
		instance.center = Vector3.from_stream(stream, instance.context, 0, None)
		instance.radius = stream.read_float()
		if instance.context.version >= 48:
			instance.num_lods_2 = stream.read_uint64()
			instance.zero = stream.read_uint64()
		if instance.context.version >= 32:
			instance.bounds_min_repeat = Vector3.from_stream(stream, instance.context, 0, None)
			instance.bounds_max_repeat = Vector3.from_stream(stream, instance.context, 0, None)
		instance.num_materials = stream.read_ushort()
		instance.num_lods = stream.read_ushort()
		instance.num_objects = stream.read_ushort()
		instance.num_meshes = stream.read_ushort()
		instance.last_count = stream.read_ushort()
		instance.render_flag = RenderFlag.from_stream(stream, instance.context, 0, None)
		instance.unks = stream.read_ushorts((7,))
		instance.pad = stream.read_ushorts((3,))
		instance.materials_ptr = stream.read_uint64()
		instance.lods_ptr = stream.read_uint64()
		instance.objects_ptr = stream.read_uint64()
		instance.models_ptr = stream.read_uint64()
		instance.first_materials_ptr = stream.read_uint64()
		if instance.context.version == 13:
			instance.zeros_ztuac = stream.read_uint64s((4,))
		instance.increment_flag = stream.read_uint64()
		instance.zero_0 = stream.read_uint64()
		if not (instance.context.version == 32):
			instance.zero_1 = stream.read_uint64()
		if instance.context.version >= 47:
			instance.zero_2 = stream.read_uint64()

	@classmethod
	def write_fields(cls, stream, instance):
		Vector3.to_stream(stream, instance.bounds_min)
		if instance.context.version >= 47:
			stream.write_float(instance.unk_float_a)
		Vector3.to_stream(stream, instance.bounds_max)
		if instance.context.version >= 47:
			stream.write_float(instance.pack_offset)
		Vector3.to_stream(stream, instance.center)
		stream.write_float(instance.radius)
		if instance.context.version >= 48:
			stream.write_uint64(instance.num_lods_2)
			stream.write_uint64(instance.zero)
		if instance.context.version >= 32:
			Vector3.to_stream(stream, instance.bounds_min_repeat)
			Vector3.to_stream(stream, instance.bounds_max_repeat)
		stream.write_ushort(instance.num_materials)
		stream.write_ushort(instance.num_lods)
		stream.write_ushort(instance.num_objects)
		stream.write_ushort(instance.num_meshes)
		stream.write_ushort(instance.last_count)
		RenderFlag.to_stream(stream, instance.render_flag)
		stream.write_ushorts(instance.unks)
		stream.write_ushorts(instance.pad)
		stream.write_uint64(instance.materials_ptr)
		stream.write_uint64(instance.lods_ptr)
		stream.write_uint64(instance.objects_ptr)
		stream.write_uint64(instance.models_ptr)
		stream.write_uint64(instance.first_materials_ptr)
		if instance.context.version == 13:
			stream.write_uint64s(instance.zeros_ztuac)
		stream.write_uint64(instance.increment_flag)
		stream.write_uint64(instance.zero_0)
		if not (instance.context.version == 32):
			stream.write_uint64(instance.zero_1)
		if instance.context.version >= 47:
			stream.write_uint64(instance.zero_2)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

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
