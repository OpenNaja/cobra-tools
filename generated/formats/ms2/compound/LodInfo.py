from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Short
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort


class LodInfo(BaseStruct):

	"""
	DLA, ZTUAC - 16 bytes
	JWE1, PZ, JWE2 - 20 bytes
	JWE2 Biosyn - 12 bytes, skips the vert / tris counts
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# FFFF
		self.full = 0

		# 7F7F
		self.half = 0

		# increasing
		self.lod_index = 0

		# usually first lod is 900
		self.distance = 0

		# always 0
		self.zero = 0

		# Last bone that is used by this lod's models; usually decreases with increasing lod index to decimate bones. However: JWE detailobjects - nat_groundcover_searocket_patchy_02 due to dedicated lod nodes
		self.bone_index = 0

		# first object for this lod in objects list
		self.first_object_index = 0
		self.first_object_index_1 = 0
		self.first_object_index_2 = 0

		# not included in interval (python style indexing)
		self.last_object_index = 0

		# vertex count of lod, sum of all vertex counts that are attached to this lod; rendered count, including duped models
		self.vertex_count = 0

		# number of index entries in the triangle index list; (not: number of triangles, byte count of tri buffer); rendered count, including duped models
		self.tri_index_count = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		if self.context.version <= 13:
			self.full = 0
			self.half = 0
			self.lod_index = 0
		if self.context.version >= 32:
			self.distance = 0.0
			self.zero = 0
		self.bone_index = 0
		self.first_object_index = 0
		if self.context.version <= 13:
			self.first_object_index_1 = 0
			self.first_object_index_2 = 0
		self.last_object_index = 0
		if self.context.version >= 32 and not ((self.context.version == 51) and self.context.biosyn):
			self.vertex_count = 0
			self.tri_index_count = 0

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
		super().read_fields(stream, instance)
		if instance.context.version <= 13:
			instance.full = stream.read_short()
			instance.half = stream.read_short()
			instance.lod_index = stream.read_ushort()
		if instance.context.version >= 32:
			instance.distance = stream.read_float()
			instance.zero = stream.read_ushort()
		instance.bone_index = stream.read_ushort()
		instance.first_object_index = stream.read_ushort()
		if instance.context.version <= 13:
			instance.first_object_index_1 = stream.read_ushort()
			instance.first_object_index_2 = stream.read_ushort()
		instance.last_object_index = stream.read_ushort()
		if instance.context.version >= 32 and not ((instance.context.version == 51) and instance.context.biosyn):
			instance.vertex_count = stream.read_uint()
			instance.tri_index_count = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.context.version <= 13:
			stream.write_short(instance.full)
			stream.write_short(instance.half)
			stream.write_ushort(instance.lod_index)
		if instance.context.version >= 32:
			stream.write_float(instance.distance)
			stream.write_ushort(instance.zero)
		stream.write_ushort(instance.bone_index)
		stream.write_ushort(instance.first_object_index)
		if instance.context.version <= 13:
			stream.write_ushort(instance.first_object_index_1)
			stream.write_ushort(instance.first_object_index_2)
		stream.write_ushort(instance.last_object_index)
		if instance.context.version >= 32 and not ((instance.context.version == 51) and instance.context.biosyn):
			stream.write_uint(instance.vertex_count)
			stream.write_uint(instance.tri_index_count)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		if instance.context.version <= 13:
			yield ('full', Short, (0, None))
			yield ('half', Short, (0, None))
			yield ('lod_index', Ushort, (0, None))
		if instance.context.version >= 32:
			yield ('distance', Float, (0, None))
			yield ('zero', Ushort, (0, None))
		yield ('bone_index', Ushort, (0, None))
		yield ('first_object_index', Ushort, (0, None))
		if instance.context.version <= 13:
			yield ('first_object_index_1', Ushort, (0, None))
			yield ('first_object_index_2', Ushort, (0, None))
		yield ('last_object_index', Ushort, (0, None))
		if instance.context.version >= 32 and not ((instance.context.version == 51) and instance.context.biosyn):
			yield ('vertex_count', Uint, (0, None))
			yield ('tri_index_count', Uint, (0, None))

	def get_info_str(self, indent=0):
		return f'LodInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* full = {self.fmt_member(self.full, indent+1)}'
		s += f'\n	* half = {self.fmt_member(self.half, indent+1)}'
		s += f'\n	* lod_index = {self.fmt_member(self.lod_index, indent+1)}'
		s += f'\n	* distance = {self.fmt_member(self.distance, indent+1)}'
		s += f'\n	* zero = {self.fmt_member(self.zero, indent+1)}'
		s += f'\n	* bone_index = {self.fmt_member(self.bone_index, indent+1)}'
		s += f'\n	* first_object_index = {self.fmt_member(self.first_object_index, indent+1)}'
		s += f'\n	* first_object_index_1 = {self.fmt_member(self.first_object_index_1, indent+1)}'
		s += f'\n	* first_object_index_2 = {self.fmt_member(self.first_object_index_2, indent+1)}'
		s += f'\n	* last_object_index = {self.fmt_member(self.last_object_index, indent+1)}'
		s += f'\n	* vertex_count = {self.fmt_member(self.vertex_count, indent+1)}'
		s += f'\n	* tri_index_count = {self.fmt_member(self.tri_index_count, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
