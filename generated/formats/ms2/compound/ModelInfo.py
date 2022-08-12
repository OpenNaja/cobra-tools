from generated.formats.base.basic import fmt_member
import generated.formats.ms2.compound.LodInfo
import generated.formats.ms2.compound.MaterialName
import generated.formats.ms2.compound.MeshDataWrap
import generated.formats.ms2.compound.Object
import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.ms2.bitfield.RenderFlag import RenderFlag
from generated.formats.ms2.compound.Vector3 import Vector3
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class ModelInfo(MemStruct):

	"""
	Describes one model, corresponding to a virtual .mdl2 file
	JWE2 - 192 bytes
	JWE2 Biosyn - 160 bytes
	There is a versioning issue introduced by the Biosyn update as the ms2 version has not been incremented
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# ??
		self.unk_dla = 0

		# the smallest coordinates across all axes
		self.bounds_min = 0

		# not sure, for PZ often 40 00 00 37 for animals
		self.unk_float_a = 0

		# the biggest coordinates across all axes
		self.bounds_max = 0

		# scale: pack_base / 512, also added as offset
		self.pack_base = 0

		# cog? medium of bounds?
		self.center = 0

		# probably from center to max
		self.radius = 0

		# seen 6 or 1, matches lod count
		self.num_lods_2 = 0

		# zero
		self.zero = 0

		# verbatim repeat
		self.bounds_min_repeat = 0

		# verbatim repeat
		self.bounds_max_repeat = 0
		self.num_materials = 0
		self.num_lods = 0
		self.num_objects = 0

		# count of MeshData fragments for the mdl2 this struct refers to
		self.num_meshes = 0

		# ?
		self.last_count = 0

		# this has influence on whether newly added shells draw correctly; for PZ usually 4, except for furry animals; ZT african ele female
		self.render_flag = 0

		# ?
		self.unks = 0
		self.pad = 0
		self.zeros = 0

		# unknown, probably used to increment skeleton
		self.increment_flag = 0
		self.zero_0 = 0
		self.zero_1 = 0
		self.zero_2 = 0
		self.materials = 0
		self.lods = 0
		self.objects = 0
		self.meshes = 0

		# points to the start of this ModelInfo's model, usually starts at materials
		# stays the same for successive mdl2s in the same model; or points to nil if no models are present
		self.first_model = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		if self.context.version <= 7:
			self.unk_dla = 0
		self.bounds_min = Vector3(self.context, 0, None)
		if self.context.version >= 47 and not ((self.context.version == 51) and self.context.biosyn):
			self.unk_float_a = 0.0
		self.bounds_max = Vector3(self.context, 0, None)
		if self.context.version >= 47 and not ((self.context.version == 51) and self.context.biosyn):
			self.pack_base = 0.0
		self.center = Vector3(self.context, 0, None)
		self.radius = 0.0
		if self.context.version >= 48 and not ((self.context.version == 51) and self.context.biosyn):
			self.num_lods_2 = 0
			self.zero = 0
		if self.context.version >= 32:
			self.bounds_min_repeat = Vector3(self.context, 0, None)
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
			self.zeros = numpy.zeros((4,), dtype=numpy.dtype('uint64'))
		if self.context.version == 7:
			self.zeros = numpy.zeros((2,), dtype=numpy.dtype('uint64'))
		self.increment_flag = 0
		if not (self.context.version == 7):
			self.zero_0 = 0
		if not (self.context.version == 32):
			self.zero_1 = 0
		if self.context.version >= 47 and not ((self.context.version == 51) and self.context.biosyn):
			self.zero_2 = 0
		self.materials = ArrayPointer(self.context, self.num_materials, generated.formats.ms2.compound.MaterialName.MaterialName)
		self.lods = ArrayPointer(self.context, self.num_lods, generated.formats.ms2.compound.LodInfo.LodInfo)
		self.objects = ArrayPointer(self.context, self.num_objects, generated.formats.ms2.compound.Object.Object)
		self.meshes = ArrayPointer(self.context, self.num_meshes, generated.formats.ms2.compound.MeshDataWrap.MeshDataWrap)
		self.first_model = Pointer(self.context, 0, None)

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
		if instance.context.version <= 7:
			instance.unk_dla = stream.read_uint64()
		instance.bounds_min = Vector3.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			instance.unk_float_a = stream.read_float()
		instance.bounds_max = Vector3.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			instance.pack_base = stream.read_float()
		instance.center = Vector3.from_stream(stream, instance.context, 0, None)
		instance.radius = stream.read_float()
		if instance.context.version >= 48 and not ((instance.context.version == 51) and instance.context.biosyn):
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
		instance.meshes = ArrayPointer.from_stream(stream, instance.context, instance.num_meshes, generated.formats.ms2.compound.MeshDataWrap.MeshDataWrap)
		instance.first_model = Pointer.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 13:
			instance.zeros = stream.read_uint64s((4,))
		if instance.context.version == 7:
			instance.zeros = stream.read_uint64s((2,))
		instance.increment_flag = stream.read_uint64()
		if not (instance.context.version == 7):
			instance.zero_0 = stream.read_uint64()
		if not (instance.context.version == 32):
			instance.zero_1 = stream.read_uint64()
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			instance.zero_2 = stream.read_uint64()
		instance.materials.arg = instance.num_materials
		instance.lods.arg = instance.num_lods
		instance.objects.arg = instance.num_objects
		instance.meshes.arg = instance.num_meshes
		instance.first_model.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.context.version <= 7:
			stream.write_uint64(instance.unk_dla)
		Vector3.to_stream(stream, instance.bounds_min)
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			stream.write_float(instance.unk_float_a)
		Vector3.to_stream(stream, instance.bounds_max)
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			stream.write_float(instance.pack_base)
		Vector3.to_stream(stream, instance.center)
		stream.write_float(instance.radius)
		if instance.context.version >= 48 and not ((instance.context.version == 51) and instance.context.biosyn):
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
		Pointer.to_stream(stream, instance.first_model)
		if instance.context.version == 13:
			stream.write_uint64s(instance.zeros)
		if instance.context.version == 7:
			stream.write_uint64s(instance.zeros)
		stream.write_uint64(instance.increment_flag)
		if not (instance.context.version == 7):
			stream.write_uint64(instance.zero_0)
		if not (instance.context.version == 32):
			stream.write_uint64(instance.zero_1)
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			stream.write_uint64(instance.zero_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		if instance.context.version <= 7:
			yield ('unk_dla', Uint64, (0, None))
		yield ('bounds_min', Vector3, (0, None))
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			yield ('unk_float_a', Float, (0, None))
		yield ('bounds_max', Vector3, (0, None))
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			yield ('pack_base', Float, (0, None))
		yield ('center', Vector3, (0, None))
		yield ('radius', Float, (0, None))
		if instance.context.version >= 48 and not ((instance.context.version == 51) and instance.context.biosyn):
			yield ('num_lods_2', Uint64, (0, None))
			yield ('zero', Uint64, (0, None))
		if instance.context.version >= 32:
			yield ('bounds_min_repeat', Vector3, (0, None))
			yield ('bounds_max_repeat', Vector3, (0, None))
		yield ('num_materials', Ushort, (0, None))
		yield ('num_lods', Ushort, (0, None))
		yield ('num_objects', Ushort, (0, None))
		yield ('num_meshes', Ushort, (0, None))
		yield ('last_count', Ushort, (0, None))
		yield ('render_flag', RenderFlag, (0, None))
		yield ('unks', Array, ((7,), Ushort, 0, None))
		yield ('pad', Array, ((3,), Ushort, 0, None))
		yield ('materials', ArrayPointer, (instance.num_materials, generated.formats.ms2.compound.MaterialName.MaterialName))
		yield ('lods', ArrayPointer, (instance.num_lods, generated.formats.ms2.compound.LodInfo.LodInfo))
		yield ('objects', ArrayPointer, (instance.num_objects, generated.formats.ms2.compound.Object.Object))
		yield ('meshes', ArrayPointer, (instance.num_meshes, generated.formats.ms2.compound.MeshDataWrap.MeshDataWrap))
		yield ('first_model', Pointer, (0, None))
		if instance.context.version == 13:
			yield ('zeros', Array, ((4,), Uint64, 0, None))
		if instance.context.version == 7:
			yield ('zeros', Array, ((2,), Uint64, 0, None))
		yield ('increment_flag', Uint64, (0, None))
		if not (instance.context.version == 7):
			yield ('zero_0', Uint64, (0, None))
		if not (instance.context.version == 32):
			yield ('zero_1', Uint64, (0, None))
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			yield ('zero_2', Uint64, (0, None))

	def get_info_str(self, indent=0):
		return f'ModelInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* unk_dla = {fmt_member(self.unk_dla, indent+1)}'
		s += f'\n	* bounds_min = {fmt_member(self.bounds_min, indent+1)}'
		s += f'\n	* unk_float_a = {fmt_member(self.unk_float_a, indent+1)}'
		s += f'\n	* bounds_max = {fmt_member(self.bounds_max, indent+1)}'
		s += f'\n	* pack_base = {fmt_member(self.pack_base, indent+1)}'
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
		s += f'\n	* first_model = {fmt_member(self.first_model, indent+1)}'
		s += f'\n	* zeros = {fmt_member(self.zeros, indent+1)}'
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
