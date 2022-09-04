import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.ms2.bitfields.RenderFlag import RenderFlag
from generated.formats.ms2.compounds.Vector3 import Vector3
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ModelInfo(MemStruct):

	"""
	Describes one model, corresponding to a virtual .mdl2 file
	JWE2 - 192 bytes
	JWE2 Biosyn - 160 bytes
	There is a versioning issue introduced by the Biosyn update as the ms2 version has not been incremented
	"""

	__name__ = 'ModelInfo'

	_import_path = 'generated.formats.ms2.compounds.ModelInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# ??
		self.unk_dla = 0

		# the smallest coordinates across all axes
		self.bounds_min = Vector3(self.context, 0, None)

		# not sure, for PZ often 40 00 00 37 for animals
		self.unk_float_a = 0.0

		# the biggest coordinates across all axes
		self.bounds_max = Vector3(self.context, 0, None)

		# scale: pack_base / 512, also added as offset
		self.pack_base = 0.0

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
		self.unks = Array(self.context, 0, None, (0,), Ushort)
		self.pad = Array(self.context, 0, None, (0,), Ushort)
		self.zeros = Array(self.context, 0, None, (0,), Uint64)

		# unknown, probably used to increment skeleton
		self.increment_flag = 0
		self.zero_0 = 0
		self.zero_1 = 0
		self.zero_2 = 0
		self.materials = ArrayPointer(self.context, self.num_materials, ModelInfo._import_path_map["generated.formats.ms2.compounds.MaterialName"])
		self.lods = ArrayPointer(self.context, self.num_lods, ModelInfo._import_path_map["generated.formats.ms2.compounds.LodInfo"])
		self.objects = ArrayPointer(self.context, self.num_objects, ModelInfo._import_path_map["generated.formats.ms2.compounds.Object"])
		self.meshes = ArrayPointer(self.context, self.num_meshes, ModelInfo._import_path_map["generated.formats.ms2.compounds.MeshDataWrap"])

		# points to the start of this ModelInfo's model, usually starts at materials
		# stays the same for successive mdl2s in the same model; or points to nil if no models are present
		self.first_model = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
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
		self.materials = ArrayPointer(self.context, self.num_materials, ModelInfo._import_path_map["generated.formats.ms2.compounds.MaterialName"])
		self.lods = ArrayPointer(self.context, self.num_lods, ModelInfo._import_path_map["generated.formats.ms2.compounds.LodInfo"])
		self.objects = ArrayPointer(self.context, self.num_objects, ModelInfo._import_path_map["generated.formats.ms2.compounds.Object"])
		self.meshes = ArrayPointer(self.context, self.num_meshes, ModelInfo._import_path_map["generated.formats.ms2.compounds.MeshDataWrap"])
		self.first_model = Pointer(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		if instance.context.version <= 7:
			instance.unk_dla = Uint64.from_stream(stream, instance.context, 0, None)
		instance.bounds_min = Vector3.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			instance.unk_float_a = Float.from_stream(stream, instance.context, 0, None)
		instance.bounds_max = Vector3.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			instance.pack_base = Float.from_stream(stream, instance.context, 0, None)
		instance.center = Vector3.from_stream(stream, instance.context, 0, None)
		instance.radius = Float.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 48 and not ((instance.context.version == 51) and instance.context.biosyn):
			instance.num_lods_2 = Uint64.from_stream(stream, instance.context, 0, None)
			instance.zero = Uint64.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 32:
			instance.bounds_min_repeat = Vector3.from_stream(stream, instance.context, 0, None)
			instance.bounds_max_repeat = Vector3.from_stream(stream, instance.context, 0, None)
		instance.num_materials = Ushort.from_stream(stream, instance.context, 0, None)
		instance.num_lods = Ushort.from_stream(stream, instance.context, 0, None)
		instance.num_objects = Ushort.from_stream(stream, instance.context, 0, None)
		instance.num_meshes = Ushort.from_stream(stream, instance.context, 0, None)
		instance.last_count = Ushort.from_stream(stream, instance.context, 0, None)
		instance.render_flag = RenderFlag.from_stream(stream, instance.context, 0, None)
		instance.unks = Array.from_stream(stream, instance.context, 0, None, (7,), Ushort)
		instance.pad = Array.from_stream(stream, instance.context, 0, None, (3,), Ushort)
		instance.materials = ArrayPointer.from_stream(stream, instance.context, instance.num_materials, ModelInfo._import_path_map["generated.formats.ms2.compounds.MaterialName"])
		instance.lods = ArrayPointer.from_stream(stream, instance.context, instance.num_lods, ModelInfo._import_path_map["generated.formats.ms2.compounds.LodInfo"])
		instance.objects = ArrayPointer.from_stream(stream, instance.context, instance.num_objects, ModelInfo._import_path_map["generated.formats.ms2.compounds.Object"])
		instance.meshes = ArrayPointer.from_stream(stream, instance.context, instance.num_meshes, ModelInfo._import_path_map["generated.formats.ms2.compounds.MeshDataWrap"])
		instance.first_model = Pointer.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 13:
			instance.zeros = Array.from_stream(stream, instance.context, 0, None, (4,), Uint64)
		if instance.context.version == 7:
			instance.zeros = Array.from_stream(stream, instance.context, 0, None, (2,), Uint64)
		instance.increment_flag = Uint64.from_stream(stream, instance.context, 0, None)
		if not (instance.context.version == 7):
			instance.zero_0 = Uint64.from_stream(stream, instance.context, 0, None)
		if not (instance.context.version == 32):
			instance.zero_1 = Uint64.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			instance.zero_2 = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.materials, int):
			instance.materials.arg = instance.num_materials
		if not isinstance(instance.lods, int):
			instance.lods.arg = instance.num_lods
		if not isinstance(instance.objects, int):
			instance.objects.arg = instance.num_objects
		if not isinstance(instance.meshes, int):
			instance.meshes.arg = instance.num_meshes
		if not isinstance(instance.first_model, int):
			instance.first_model.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.context.version <= 7:
			Uint64.to_stream(stream, instance.unk_dla)
		Vector3.to_stream(stream, instance.bounds_min)
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			Float.to_stream(stream, instance.unk_float_a)
		Vector3.to_stream(stream, instance.bounds_max)
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			Float.to_stream(stream, instance.pack_base)
		Vector3.to_stream(stream, instance.center)
		Float.to_stream(stream, instance.radius)
		if instance.context.version >= 48 and not ((instance.context.version == 51) and instance.context.biosyn):
			Uint64.to_stream(stream, instance.num_lods_2)
			Uint64.to_stream(stream, instance.zero)
		if instance.context.version >= 32:
			Vector3.to_stream(stream, instance.bounds_min_repeat)
			Vector3.to_stream(stream, instance.bounds_max_repeat)
		Ushort.to_stream(stream, instance.num_materials)
		Ushort.to_stream(stream, instance.num_lods)
		Ushort.to_stream(stream, instance.num_objects)
		Ushort.to_stream(stream, instance.num_meshes)
		Ushort.to_stream(stream, instance.last_count)
		RenderFlag.to_stream(stream, instance.render_flag)
		Array.to_stream(stream, instance.unks, instance.context, 0, None, (7,), Ushort)
		Array.to_stream(stream, instance.pad, instance.context, 0, None, (3,), Ushort)
		ArrayPointer.to_stream(stream, instance.materials)
		ArrayPointer.to_stream(stream, instance.lods)
		ArrayPointer.to_stream(stream, instance.objects)
		ArrayPointer.to_stream(stream, instance.meshes)
		Pointer.to_stream(stream, instance.first_model)
		if instance.context.version == 13:
			Array.to_stream(stream, instance.zeros, instance.context, 0, None, (4,), Uint64)
		if instance.context.version == 7:
			Array.to_stream(stream, instance.zeros, instance.context, 0, None, (2,), Uint64)
		Uint64.to_stream(stream, instance.increment_flag)
		if not (instance.context.version == 7):
			Uint64.to_stream(stream, instance.zero_0)
		if not (instance.context.version == 32):
			Uint64.to_stream(stream, instance.zero_1)
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			Uint64.to_stream(stream, instance.zero_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		if instance.context.version <= 7:
			yield 'unk_dla', Uint64, (0, None), (False, None)
		yield 'bounds_min', Vector3, (0, None), (False, None)
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			yield 'unk_float_a', Float, (0, None), (False, None)
		yield 'bounds_max', Vector3, (0, None), (False, None)
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			yield 'pack_base', Float, (0, None), (False, None)
		yield 'center', Vector3, (0, None), (False, None)
		yield 'radius', Float, (0, None), (False, None)
		if instance.context.version >= 48 and not ((instance.context.version == 51) and instance.context.biosyn):
			yield 'num_lods_2', Uint64, (0, None), (False, None)
			yield 'zero', Uint64, (0, None), (False, None)
		if instance.context.version >= 32:
			yield 'bounds_min_repeat', Vector3, (0, None), (False, None)
			yield 'bounds_max_repeat', Vector3, (0, None), (False, None)
		yield 'num_materials', Ushort, (0, None), (False, None)
		yield 'num_lods', Ushort, (0, None), (False, None)
		yield 'num_objects', Ushort, (0, None), (False, None)
		yield 'num_meshes', Ushort, (0, None), (False, None)
		yield 'last_count', Ushort, (0, None), (False, None)
		yield 'render_flag', RenderFlag, (0, None), (False, None)
		yield 'unks', Array, (0, None, (7,), Ushort), (False, None)
		yield 'pad', Array, (0, None, (3,), Ushort), (False, None)
		yield 'materials', ArrayPointer, (instance.num_materials, ModelInfo._import_path_map["generated.formats.ms2.compounds.MaterialName"]), (False, None)
		yield 'lods', ArrayPointer, (instance.num_lods, ModelInfo._import_path_map["generated.formats.ms2.compounds.LodInfo"]), (False, None)
		yield 'objects', ArrayPointer, (instance.num_objects, ModelInfo._import_path_map["generated.formats.ms2.compounds.Object"]), (False, None)
		yield 'meshes', ArrayPointer, (instance.num_meshes, ModelInfo._import_path_map["generated.formats.ms2.compounds.MeshDataWrap"]), (False, None)
		yield 'first_model', Pointer, (0, None), (False, None)
		if instance.context.version == 13:
			yield 'zeros', Array, (0, None, (4,), Uint64), (False, None)
		if instance.context.version == 7:
			yield 'zeros', Array, (0, None, (2,), Uint64), (False, None)
		yield 'increment_flag', Uint64, (0, None), (False, None)
		if not (instance.context.version == 7):
			yield 'zero_0', Uint64, (0, None), (False, None)
		if not (instance.context.version == 32):
			yield 'zero_1', Uint64, (0, None), (False, None)
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			yield 'zero_2', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'ModelInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* unk_dla = {self.fmt_member(self.unk_dla, indent+1)}'
		s += f'\n	* bounds_min = {self.fmt_member(self.bounds_min, indent+1)}'
		s += f'\n	* unk_float_a = {self.fmt_member(self.unk_float_a, indent+1)}'
		s += f'\n	* bounds_max = {self.fmt_member(self.bounds_max, indent+1)}'
		s += f'\n	* pack_base = {self.fmt_member(self.pack_base, indent+1)}'
		s += f'\n	* center = {self.fmt_member(self.center, indent+1)}'
		s += f'\n	* radius = {self.fmt_member(self.radius, indent+1)}'
		s += f'\n	* num_lods_2 = {self.fmt_member(self.num_lods_2, indent+1)}'
		s += f'\n	* zero = {self.fmt_member(self.zero, indent+1)}'
		s += f'\n	* bounds_min_repeat = {self.fmt_member(self.bounds_min_repeat, indent+1)}'
		s += f'\n	* bounds_max_repeat = {self.fmt_member(self.bounds_max_repeat, indent+1)}'
		s += f'\n	* num_materials = {self.fmt_member(self.num_materials, indent+1)}'
		s += f'\n	* num_lods = {self.fmt_member(self.num_lods, indent+1)}'
		s += f'\n	* num_objects = {self.fmt_member(self.num_objects, indent+1)}'
		s += f'\n	* num_meshes = {self.fmt_member(self.num_meshes, indent+1)}'
		s += f'\n	* last_count = {self.fmt_member(self.last_count, indent+1)}'
		s += f'\n	* render_flag = {self.fmt_member(self.render_flag, indent+1)}'
		s += f'\n	* unks = {self.fmt_member(self.unks, indent+1)}'
		s += f'\n	* pad = {self.fmt_member(self.pad, indent+1)}'
		s += f'\n	* materials = {self.fmt_member(self.materials, indent+1)}'
		s += f'\n	* lods = {self.fmt_member(self.lods, indent+1)}'
		s += f'\n	* objects = {self.fmt_member(self.objects, indent+1)}'
		s += f'\n	* meshes = {self.fmt_member(self.meshes, indent+1)}'
		s += f'\n	* first_model = {self.fmt_member(self.first_model, indent+1)}'
		s += f'\n	* zeros = {self.fmt_member(self.zeros, indent+1)}'
		s += f'\n	* increment_flag = {self.fmt_member(self.increment_flag, indent+1)}'
		s += f'\n	* zero_0 = {self.fmt_member(self.zero_0, indent+1)}'
		s += f'\n	* zero_1 = {self.fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* zero_2 = {self.fmt_member(self.zero_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
