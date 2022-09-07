from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.ms2.compounds.DLAPreBones import DLAPreBones
from generated.formats.ms2.compounds.FloatsY import FloatsY
from generated.formats.ms2.compounds.LodInfo import LodInfo
from generated.formats.ms2.compounds.MaterialName import MaterialName
from generated.formats.ms2.compounds.MeshDataWrap import MeshDataWrap
from generated.formats.ms2.compounds.Object import Object
from generated.formats.ms2.compounds.ZTPreBones import ZTPreBones


class Model(BaseStruct):

	__name__ = 'Model'

	_import_path = 'generated.formats.ms2.compounds.Model'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# name pointers for each material
		self.materials = Array(self.context, 0, None, (0,), MaterialName)

		# lod info for each level, only present if models are present (despite the count sometimes saying otherwise!)
		self.lods = Array(self.context, 0, None, (0,), LodInfo)

		# instantiate the meshes with materials
		self.objects = Array(self.context, 0, None, (0,), Object)

		# pad to 8 bytes alignment
		# rhino: start of model - end of objects: 124 - 4 bytes padding
		# ele: start of model - end of objects: 120 - 0 bytes padding
		self.objects_padding = 0

		# mesh data blocks for this model
		self.meshes = Array(self.context, 0, None, (0,), MeshDataWrap)

		# ?
		self.pre_bones = DLAPreBones(self.context, 0, None)

		# see if it is a flag for ztuac too, so might be totally wrong here
		self.floatsy = Array(self.context, 0, None, (0,), FloatsY)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.materials = Array(self.context, 0, None, (self.arg.num_materials,), MaterialName)
		self.lods = Array(self.context, 0, None, (self.arg.num_lods,), LodInfo)
		self.objects = Array(self.context, 0, None, (self.arg.num_objects,), Object)
		if self.context.version <= 13 and (self.arg.num_materials + self.arg.num_objects) % 2:
			self.objects_padding = 0
		self.meshes = Array(self.context, 0, None, (self.arg.num_meshes,), MeshDataWrap)
		if self.context.version == 13 and self.arg.last_count:
			self.pre_bones = ZTPreBones(self.context, 0, None)
		if self.context.version == 7 and self.arg.last_count:
			self.pre_bones = DLAPreBones(self.context, 0, None)
		if self.context.version <= 32:
			self.floatsy = Array(self.context, 0, None, (self.arg.render_flag,), FloatsY)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.materials = Array.from_stream(stream, instance.context, 0, None, (instance.arg.num_materials,), MaterialName)
		instance.lods = Array.from_stream(stream, instance.context, 0, None, (instance.arg.num_lods,), LodInfo)
		instance.objects = Array.from_stream(stream, instance.context, 0, None, (instance.arg.num_objects,), Object)
		if instance.context.version <= 13 and (instance.arg.num_materials + instance.arg.num_objects) % 2:
			instance.objects_padding = Uint.from_stream(stream, instance.context, 0, None)
		instance.meshes = Array.from_stream(stream, instance.context, 0, None, (instance.arg.num_meshes,), MeshDataWrap)
		if instance.context.version == 13 and instance.arg.last_count:
			instance.pre_bones = ZTPreBones.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 7 and instance.arg.last_count:
			instance.pre_bones = DLAPreBones.from_stream(stream, instance.context, 0, None)
		if instance.context.version <= 32:
			instance.floatsy = Array.from_stream(stream, instance.context, 0, None, (instance.arg.render_flag,), FloatsY)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.materials, instance.context, 0, None, (instance.arg.num_materials,), MaterialName)
		Array.to_stream(stream, instance.lods, instance.context, 0, None, (instance.arg.num_lods,), LodInfo)
		Array.to_stream(stream, instance.objects, instance.context, 0, None, (instance.arg.num_objects,), Object)
		if instance.context.version <= 13 and (instance.arg.num_materials + instance.arg.num_objects) % 2:
			Uint.to_stream(stream, instance.objects_padding)
		Array.to_stream(stream, instance.meshes, instance.context, 0, None, (instance.arg.num_meshes,), MeshDataWrap)
		if instance.context.version == 13 and instance.arg.last_count:
			ZTPreBones.to_stream(stream, instance.pre_bones)
		if instance.context.version == 7 and instance.arg.last_count:
			DLAPreBones.to_stream(stream, instance.pre_bones)
		if instance.context.version <= 32:
			Array.to_stream(stream, instance.floatsy, instance.context, 0, None, (instance.arg.render_flag,), FloatsY)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'materials', Array, (0, None, (instance.arg.num_materials,), MaterialName), (False, None)
		yield 'lods', Array, (0, None, (instance.arg.num_lods,), LodInfo), (False, None)
		yield 'objects', Array, (0, None, (instance.arg.num_objects,), Object), (False, None)
		if instance.context.version <= 13 and (instance.arg.num_materials + instance.arg.num_objects) % 2:
			yield 'objects_padding', Uint, (0, None), (False, None)
		yield 'meshes', Array, (0, None, (instance.arg.num_meshes,), MeshDataWrap), (False, None)
		if instance.context.version == 13 and instance.arg.last_count:
			yield 'pre_bones', ZTPreBones, (0, None), (False, None)
		if instance.context.version == 7 and instance.arg.last_count:
			yield 'pre_bones', DLAPreBones, (0, None), (False, None)
		if instance.context.version <= 32:
			yield 'floatsy', Array, (0, None, (instance.arg.render_flag,), FloatsY), (False, None)

	def get_info_str(self, indent=0):
		return f'Model [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
