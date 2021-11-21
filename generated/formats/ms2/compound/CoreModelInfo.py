import numpy
from generated.context import ContextReference
from generated.formats.ms2.bitfield.RenderFlag import RenderFlag
from generated.formats.ms2.compound.Vector3 import Vector3


class CoreModelInfo:

	"""
	Used by ms2 or in Mdl2ModelInfo
	In load order it always defines the variable fragments for the next mdl2
	The mdl2's fragment informs the first mdl2
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

		# PZ only, zero-ish
		self.unknowns = numpy.zeros((4,), dtype=numpy.dtype('float32'))

		# verbatim repeat
		self.bounds_min_repeat = Vector3(self.context, 0, None)

		# verbatim repeat
		self.bounds_max_repeat = Vector3(self.context, 0, None)
		self.num_materials = 0
		self.num_lods = 0
		self.num_objects = 0

		# count of modeldata fragments for the mdl2 this struct refers to
		self.num_models = 0

		# ?
		self.last_count = 0

		# this has influence on whether newly added shells draw correctly; for PZ usually 4, except for furry animals; ZT african ele female
		self.render_flag = RenderFlag(self.context, 0, None)

		# ?
		self.unks = numpy.zeros((7,), dtype=numpy.dtype('uint16'))
		self.pad = numpy.zeros((3,), dtype=numpy.dtype('uint16'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.bounds_min = Vector3(self.context, 0, None)
		if not (self.context.version < 19):
			self.unk_float_a = 0.0
		self.bounds_max = Vector3(self.context, 0, None)
		if not (self.context.version < 19):
			self.pack_offset = 0.0
		self.center = Vector3(self.context, 0, None)
		self.radius = 0.0
		if ((not self.context.user_version.is_jwe) and (self.context.version >= 19)) or (self.context.user_version.is_jwe and (self.context.version == 20)):
			self.unknowns = numpy.zeros((4,), dtype=numpy.dtype('float32'))
		if not (self.context.version == 17):
			self.bounds_min_repeat = Vector3(self.context, 0, None)
		if not (self.context.version == 17):
			self.bounds_max_repeat = Vector3(self.context, 0, None)
		self.num_materials = 0
		self.num_lods = 0
		self.num_objects = 0
		self.num_models = 0
		self.last_count = 0
		self.render_flag = RenderFlag(self.context, 0, None)
		self.unks = numpy.zeros((7,), dtype=numpy.dtype('uint16'))
		self.pad = numpy.zeros((3,), dtype=numpy.dtype('uint16'))

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
		if not (instance.context.version < 19):
			instance.unk_float_a = stream.read_float()
		instance.bounds_max = Vector3.from_stream(stream, instance.context, 0, None)
		if not (instance.context.version < 19):
			instance.pack_offset = stream.read_float()
		instance.center = Vector3.from_stream(stream, instance.context, 0, None)
		instance.radius = stream.read_float()
		if ((not instance.context.user_version.is_jwe) and (instance.context.version >= 19)) or (instance.context.user_version.is_jwe and (instance.context.version == 20)):
			instance.unknowns = stream.read_floats((4,))
		if not (instance.context.version == 17):
			instance.bounds_min_repeat = Vector3.from_stream(stream, instance.context, 0, None)
			instance.bounds_max_repeat = Vector3.from_stream(stream, instance.context, 0, None)
		instance.num_materials = stream.read_ushort()
		instance.num_lods = stream.read_ushort()
		instance.num_objects = stream.read_ushort()
		instance.num_models = stream.read_ushort()
		instance.last_count = stream.read_ushort()
		instance.render_flag = RenderFlag.from_stream(stream, instance.context, 0, None)
		instance.unks = stream.read_ushorts((7,))
		instance.pad = stream.read_ushorts((3,))

	@classmethod
	def write_fields(cls, stream, instance):
		Vector3.to_stream(stream, instance.bounds_min)
		if not (instance.context.version < 19):
			stream.write_float(instance.unk_float_a)
		Vector3.to_stream(stream, instance.bounds_max)
		if not (instance.context.version < 19):
			stream.write_float(instance.pack_offset)
		Vector3.to_stream(stream, instance.center)
		stream.write_float(instance.radius)
		if ((not instance.context.user_version.is_jwe) and (instance.context.version >= 19)) or (instance.context.user_version.is_jwe and (instance.context.version == 20)):
			stream.write_floats(instance.unknowns)
		if not (instance.context.version == 17):
			Vector3.to_stream(stream, instance.bounds_min_repeat)
			Vector3.to_stream(stream, instance.bounds_max_repeat)
		stream.write_ushort(instance.num_materials)
		stream.write_ushort(instance.num_lods)
		stream.write_ushort(instance.num_objects)
		stream.write_ushort(instance.num_models)
		stream.write_ushort(instance.last_count)
		RenderFlag.to_stream(stream, instance.render_flag)
		stream.write_ushorts(instance.unks)
		stream.write_ushorts(instance.pad)

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
		s += f'\n	* num_materials = {self.num_materials.__repr__()}'
		s += f'\n	* num_lods = {self.num_lods.__repr__()}'
		s += f'\n	* num_objects = {self.num_objects.__repr__()}'
		s += f'\n	* num_models = {self.num_models.__repr__()}'
		s += f'\n	* last_count = {self.last_count.__repr__()}'
		s += f'\n	* render_flag = {self.render_flag.__repr__()}'
		s += f'\n	* unks = {self.unks.__repr__()}'
		s += f'\n	* pad = {self.pad.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
