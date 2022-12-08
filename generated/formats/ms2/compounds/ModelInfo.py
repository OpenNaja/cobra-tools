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

	_import_key = 'ms2.compounds.ModelInfo'

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
		self.materials = ArrayPointer(self.context, self.num_materials, ModelInfo._import_map["ms2.compounds.MaterialName"])
		self.lods = ArrayPointer(self.context, self.num_lods, ModelInfo._import_map["ms2.compounds.LodInfo"])
		self.objects = ArrayPointer(self.context, self.num_objects, ModelInfo._import_map["ms2.compounds.Object"])
		self.meshes = ArrayPointer(self.context, self.num_meshes, ModelInfo._import_map["ms2.compounds.MeshDataWrap"])

		# points to the start of this ModelInfo's model, usually starts at materials
		# stays the same for successive mdl2s in the same model; or points to nil if no models are present
		self.first_model = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('unk_dla', Uint64, (0, None), (False, None), True),
		('bounds_min', Vector3, (0, None), (False, None), None),
		('unk_float_a', Float, (0, None), (False, None), True),
		('bounds_max', Vector3, (0, None), (False, None), None),
		('pack_base', Float, (0, None), (False, None), True),
		('center', Vector3, (0, None), (False, None), None),
		('radius', Float, (0, None), (False, None), None),
		('num_lods_2', Uint64, (0, None), (False, None), True),
		('zero', Uint64, (0, None), (False, None), True),
		('bounds_min_repeat', Vector3, (0, None), (False, None), True),
		('bounds_max_repeat', Vector3, (0, None), (False, None), True),
		('num_materials', Ushort, (0, None), (False, None), None),
		('num_lods', Ushort, (0, None), (False, None), None),
		('num_objects', Ushort, (0, None), (False, None), None),
		('num_meshes', Ushort, (0, None), (False, None), None),
		('last_count', Ushort, (0, None), (False, None), None),
		('render_flag', RenderFlag, (0, None), (False, None), None),
		('unks', Array, (0, None, (7,), Ushort), (False, None), None),
		('pad', Array, (0, None, (3,), Ushort), (False, None), None),
		('materials', ArrayPointer, (None, None), (False, None), None),
		('lods', ArrayPointer, (None, None), (False, None), None),
		('objects', ArrayPointer, (None, None), (False, None), None),
		('meshes', ArrayPointer, (None, None), (False, None), None),
		('first_model', Pointer, (0, None), (False, None), None),
		('zeros', Array, (0, None, (4,), Uint64), (False, None), True),
		('zeros', Array, (0, None, (2,), Uint64), (False, None), True),
		('increment_flag', Uint64, (0, None), (False, None), None),
		('zero_0', Uint64, (0, None), (False, None), True),
		('zero_1', Uint64, (0, None), (False, None), True),
		('zero_2', Uint64, (0, None), (False, None), True),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version <= 7:
			yield 'unk_dla', Uint64, (0, None), (False, None)
		yield 'bounds_min', Vector3, (0, None), (False, None)
		if instance.context.version >= 47 and not (((instance.context.version == 51) or (instance.context.version == 52)) and instance.context.biosyn):
			yield 'unk_float_a', Float, (0, None), (False, None)
		yield 'bounds_max', Vector3, (0, None), (False, None)
		if instance.context.version >= 47 and not (((instance.context.version == 51) or (instance.context.version == 52)) and instance.context.biosyn):
			yield 'pack_base', Float, (0, None), (False, None)
		yield 'center', Vector3, (0, None), (False, None)
		yield 'radius', Float, (0, None), (False, None)
		if instance.context.version >= 48 and not (((instance.context.version == 51) or (instance.context.version == 52)) and instance.context.biosyn):
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
		yield 'materials', ArrayPointer, (instance.num_materials, ModelInfo._import_map["ms2.compounds.MaterialName"]), (False, None)
		yield 'lods', ArrayPointer, (instance.num_lods, ModelInfo._import_map["ms2.compounds.LodInfo"]), (False, None)
		yield 'objects', ArrayPointer, (instance.num_objects, ModelInfo._import_map["ms2.compounds.Object"]), (False, None)
		yield 'meshes', ArrayPointer, (instance.num_meshes, ModelInfo._import_map["ms2.compounds.MeshDataWrap"]), (False, None)
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
		if instance.context.version >= 47 and not (((instance.context.version == 51) or (instance.context.version == 52)) and instance.context.biosyn):
			yield 'zero_2', Uint64, (0, None), (False, None)
