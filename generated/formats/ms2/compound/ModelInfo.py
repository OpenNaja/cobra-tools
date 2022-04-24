from source.formats.base.basic import fmt_member
import generated.formats.ms2.compound.LodInfo
import generated.formats.ms2.compound.MaterialName
import generated.formats.ms2.compound.NewMeshData
import generated.formats.ms2.compound.Object
import numpy
from generated.formats.ms2.bitfield.RenderFlag import RenderFlag
from generated.formats.ms2.compound.Vector3 import Vector3
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class ModelInfo(MemStruct):

	"""
	Linked to by the ms2, part of an array
	120 bytes for JWE2
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
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
		self.zeros_ztuac = numpy.zeros((4,), dtype=numpy.dtype('uint64'))

		# unknown, probably used to increment skeleton
		self.increment_flag = 0
		self.zero_0 = 0
		self.zero_1 = 0
		self.zero_2 = 0
		self.materials = ArrayPointer(self.context, self.num_materials, generated.formats.ms2.compound.MaterialName.MaterialName)
		self.lods = ArrayPointer(self.context, self.num_lods, generated.formats.ms2.compound.LodInfo.LodInfo)
		self.objects = ArrayPointer(self.context, self.num_objects, generated.formats.ms2.compound.Object.Object)
		self.meshes = ArrayPointer(self.context, self.num_meshes, generated.formats.ms2.compound.NewMeshData.NewMeshData)

		# actually points to the start of ModelInfos array
		self.first_materials = Pointer(self.context, 0, None)
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
		if self.context.version == 13:
			self.zeros_ztuac = numpy.zeros((4,), dtype=numpy.dtype('uint64'))
		self.increment_flag = 0
		self.zero_0 = 0
		if not (self.context.version == 32):
			self.zero_1 = 0
		if self.context.version >= 47:
			self.zero_2 = 0
		self.materials = ArrayPointer(self.context, self.num_materials, generated.formats.ms2.compound.MaterialName.MaterialName)
		self.lods = ArrayPointer(self.context, self.num_lods, generated.formats.ms2.compound.LodInfo.LodInfo)
		self.objects = ArrayPointer(self.context, self.num_objects, generated.formats.ms2.compound.Object.Object)
		self.meshes = ArrayPointer(self.context, self.num_meshes, generated.formats.ms2.compound.NewMeshData.NewMeshData)
		self.first_materials = Pointer(self.context, 0, None)

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
		instance.materials = ArrayPointer.from_stream(stream, instance.context, instance.num_materials, generated.formats.ms2.compound.MaterialName.MaterialName)
		instance.lods = ArrayPointer.from_stream(stream, instance.context, instance.num_lods, generated.formats.ms2.compound.LodInfo.LodInfo)
		instance.objects = ArrayPointer.from_stream(stream, instance.context, instance.num_objects, generated.formats.ms2.compound.Object.Object)
		instance.meshes = ArrayPointer.from_stream(stream, instance.context, instance.num_meshes, generated.formats.ms2.compound.NewMeshData.NewMeshData)
		instance.first_materials = Pointer.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 13:
			instance.zeros_ztuac = stream.read_uint64s((4,))
		instance.increment_flag = stream.read_uint64()
		instance.zero_0 = stream.read_uint64()
		if not (instance.context.version == 32):
			instance.zero_1 = stream.read_uint64()
		if instance.context.version >= 47:
			instance.zero_2 = stream.read_uint64()
		instance.materials.arg = instance.num_materials
		instance.lods.arg = instance.num_lods
		instance.objects.arg = instance.num_objects
		instance.meshes.arg = instance.num_meshes
		instance.first_materials.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
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
		ArrayPointer.to_stream(stream, instance.materials)
		ArrayPointer.to_stream(stream, instance.lods)
		ArrayPointer.to_stream(stream, instance.objects)
		ArrayPointer.to_stream(stream, instance.meshes)
		Pointer.to_stream(stream, instance.first_materials)
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

	def get_info_str(self, indent=0):
		return f'ModelInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* bounds_min = {fmt_member(self.bounds_min, indent+1)}'
		s += f'\n	* unk_float_a = {fmt_member(self.unk_float_a, indent+1)}'
		s += f'\n	* bounds_max = {fmt_member(self.bounds_max, indent+1)}'
		s += f'\n	* pack_offset = {fmt_member(self.pack_offset, indent+1)}'
		s += f'\n	* center = {fmt_member(self.center, indent+1)}'
		s += f'\n	* radius = {fmt_member(self.radius, indent+1)}'
		s += f'\n	* num_lods_2 = {fmt_member(self.num_lods_2, indent+1)}'
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		s += f'\n	* bounds_min_repeat = {fmt_member(self.bounds_min_repeat, indent+1)}'
		s += f'\n	* bounds_max_repeat = {fmt_member(self.bounds_max_repeat, indent+1)}'
		s += f'\n	* num_materials = {fmt_member(self.num_materials, indent+1)}'
		s += f'\n	* num_lods = {fmt_member(self.num_lods, indent+1)}'
		s += f'\n	* num_objects = {fmt_member(self.num_objects, indent+1)}'
		s += f'\n	* num_meshes = {fmt_member(self.num_meshes, indent+1)}'
		s += f'\n	* last_count = {fmt_member(self.last_count, indent+1)}'
		s += f'\n	* render_flag = {fmt_member(self.render_flag, indent+1)}'
		s += f'\n	* unks = {fmt_member(self.unks, indent+1)}'
		s += f'\n	* pad = {fmt_member(self.pad, indent+1)}'
		s += f'\n	* materials = {fmt_member(self.materials, indent+1)}'
		s += f'\n	* lods = {fmt_member(self.lods, indent+1)}'
		s += f'\n	* objects = {fmt_member(self.objects, indent+1)}'
		s += f'\n	* meshes = {fmt_member(self.meshes, indent+1)}'
		s += f'\n	* first_materials = {fmt_member(self.first_materials, indent+1)}'
		s += f'\n	* zeros_ztuac = {fmt_member(self.zeros_ztuac, indent+1)}'
		s += f'\n	* increment_flag = {fmt_member(self.increment_flag, indent+1)}'
		s += f'\n	* zero_0 = {fmt_member(self.zero_0, indent+1)}'
		s += f'\n	* zero_1 = {fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* zero_2 = {fmt_member(self.zero_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
