from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.FloatsY import FloatsY
from generated.formats.ms2.compound.LodInfo import LodInfo
from generated.formats.ms2.compound.LodInfoZT import LodInfoZT
from generated.formats.ms2.compound.MaterialName import MaterialName
from generated.formats.ms2.compound.NewMeshData import NewMeshData
from generated.formats.ms2.compound.Object import Object
from generated.formats.ms2.compound.PcMeshData import PcMeshData
from generated.formats.ms2.compound.ZTPreBones import ZTPreBones
from generated.formats.ms2.compound.ZtMeshData import ZtMeshData


class Model:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# name pointers for each material
		self.materials = Array((self.arg.num_materials,), MaterialName, self.context, 0, None)
		self.lods = Array((self.arg.num_lods,), LodInfoZT, self.context, 0, None)

		# lod info for each level, only present if models are present (despite the count sometimes saying otherwise!)
		self.lods = Array((self.arg.num_lods,), LodInfo, self.context, 0, None)

		# instantiate the meshes with materials
		self.objects = Array((self.arg.num_objects,), Object, self.context, 0, None)

		# pad to 8 bytes alignment
		# rhino: start of model - end of objects: 124 - 4 bytes padding
		# ele: start of model - end of objects: 120 - 0 bytes padding
		self.objects_padding = 0

		# mesh data blocks for this model
		self.meshes = Array((self.arg.num_meshes,), NewMeshData, self.context, 0, None)
		self.meshes = Array((self.arg.num_meshes,), PcMeshData, self.context, 0, None)
		self.meshes = Array((self.arg.num_meshes,), ZtMeshData, self.context, 0, None)

		# ?
		self.ztuac_pre_bones = ZTPreBones(self.context, 0, None)

		# see if it is a flag for ztuac too, so might be totally wrong here
		self.floatsy = Array((self.arg.render_flag,), FloatsY, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.materials = Array((self.arg.num_materials,), MaterialName, self.context, 0, None)
		if self.context.version <= 13:
			self.lods = Array((self.arg.num_lods,), LodInfoZT, self.context, 0, None)
		if self.context.version >= 32 and self.arg.num_meshes:
			self.lods = Array((self.arg.num_lods,), LodInfo, self.context, 0, None)
		self.objects = Array((self.arg.num_objects,), Object, self.context, 0, None)
		if self.context.version <= 13 and (self.arg.num_materials + self.arg.num_objects) % 2:
			self.objects_padding = 0
		if self.context.version >= 47:
			self.meshes = Array((self.arg.num_meshes,), NewMeshData, self.context, 0, None)
		if self.context.version == 32:
			self.meshes = Array((self.arg.num_meshes,), PcMeshData, self.context, 0, None)
		if self.context.version == 13:
			self.meshes = Array((self.arg.num_meshes,), ZtMeshData, self.context, 0, None)
		if self.context.version == 13 and self.arg.last_count:
			self.ztuac_pre_bones = ZTPreBones(self.context, 0, None)
		if self.context.version <= 32:
			self.floatsy = Array((self.arg.render_flag,), FloatsY, self.context, 0, None)

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
		instance.materials = Array.from_stream(stream, (instance.arg.num_materials,), MaterialName, instance.context, 0, None)
		if instance.context.version <= 13:
			instance.lods = Array.from_stream(stream, (instance.arg.num_lods,), LodInfoZT, instance.context, 0, None)
		if instance.context.version >= 32 and instance.arg.num_meshes:
			instance.lods = Array.from_stream(stream, (instance.arg.num_lods,), LodInfo, instance.context, 0, None)
		instance.objects = Array.from_stream(stream, (instance.arg.num_objects,), Object, instance.context, 0, None)
		if instance.context.version <= 13 and (instance.arg.num_materials + instance.arg.num_objects) % 2:
			instance.objects_padding = stream.read_uint()
		if instance.context.version >= 47:
			instance.meshes = Array.from_stream(stream, (instance.arg.num_meshes,), NewMeshData, instance.context, 0, None)
		if instance.context.version == 32:
			instance.meshes = Array.from_stream(stream, (instance.arg.num_meshes,), PcMeshData, instance.context, 0, None)
		if instance.context.version == 13:
			instance.meshes = Array.from_stream(stream, (instance.arg.num_meshes,), ZtMeshData, instance.context, 0, None)
		if instance.context.version == 13 and instance.arg.last_count:
			instance.ztuac_pre_bones = ZTPreBones.from_stream(stream, instance.context, 0, None)
		if instance.context.version <= 32:
			instance.floatsy = Array.from_stream(stream, (instance.arg.render_flag,), FloatsY, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		Array.to_stream(stream, instance.materials, (instance.arg.num_materials,), MaterialName, instance.context, 0, None)
		if instance.context.version <= 13:
			Array.to_stream(stream, instance.lods, (instance.arg.num_lods,), LodInfoZT, instance.context, 0, None)
		if instance.context.version >= 32 and instance.arg.num_meshes:
			Array.to_stream(stream, instance.lods, (instance.arg.num_lods,), LodInfo, instance.context, 0, None)
		Array.to_stream(stream, instance.objects, (instance.arg.num_objects,), Object, instance.context, 0, None)
		if instance.context.version <= 13 and (instance.arg.num_materials + instance.arg.num_objects) % 2:
			stream.write_uint(instance.objects_padding)
		if instance.context.version >= 47:
			Array.to_stream(stream, instance.meshes, (instance.arg.num_meshes,), NewMeshData, instance.context, 0, None)
		if instance.context.version == 32:
			Array.to_stream(stream, instance.meshes, (instance.arg.num_meshes,), PcMeshData, instance.context, 0, None)
		if instance.context.version == 13:
			Array.to_stream(stream, instance.meshes, (instance.arg.num_meshes,), ZtMeshData, instance.context, 0, None)
		if instance.context.version == 13 and instance.arg.last_count:
			ZTPreBones.to_stream(stream, instance.ztuac_pre_bones)
		if instance.context.version <= 32:
			Array.to_stream(stream, instance.floatsy, (instance.arg.render_flag,), FloatsY, instance.context, 0, None)

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
		return f'Model [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* materials = {self.materials.__repr__()}'
		s += f'\n	* lods = {self.lods.__repr__()}'
		s += f'\n	* objects = {self.objects.__repr__()}'
		s += f'\n	* objects_padding = {self.objects_padding.__repr__()}'
		s += f'\n	* meshes = {self.meshes.__repr__()}'
		s += f'\n	* ztuac_pre_bones = {self.ztuac_pre_bones.__repr__()}'
		s += f'\n	* floatsy = {self.floatsy.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
