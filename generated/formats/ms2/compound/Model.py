from source.formats.base.basic import fmt_member
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.DLAPreBones import DLAPreBones
from generated.formats.ms2.compound.FloatsY import FloatsY
from generated.formats.ms2.compound.LodInfo import LodInfo
from generated.formats.ms2.compound.MaterialName import MaterialName
from generated.formats.ms2.compound.MeshDataWrap import MeshDataWrap
from generated.formats.ms2.compound.Object import Object
from generated.formats.ms2.compound.ZTPreBones import ZTPreBones


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

		# lod info for each level, only present if models are present (despite the count sometimes saying otherwise!)
		self.lods = Array((self.arg.num_lods,), LodInfo, self.context, 0, None)

		# instantiate the meshes with materials
		self.objects = Array((self.arg.num_objects,), Object, self.context, 0, None)

		# pad to 8 bytes alignment
		# rhino: start of model - end of objects: 124 - 4 bytes padding
		# ele: start of model - end of objects: 120 - 0 bytes padding
		self.objects_padding = 0

		# mesh data blocks for this model
		self.meshes = Array((self.arg.num_meshes,), MeshDataWrap, self.context, 0, None)

		# ?
		self.pre_bones = ZTPreBones(self.context, 0, None)

		# ?
		self.pre_bones = DLAPreBones(self.context, 0, None)

		# see if it is a flag for ztuac too, so might be totally wrong here
		self.floatsy = Array((self.arg.render_flag,), FloatsY, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.materials = Array((self.arg.num_materials,), MaterialName, self.context, 0, None)
		self.lods = Array((self.arg.num_lods,), LodInfo, self.context, 0, None)
		self.objects = Array((self.arg.num_objects,), Object, self.context, 0, None)
		if self.context.version <= 13 and (self.arg.num_materials + self.arg.num_objects) % 2:
			self.objects_padding = 0
		self.meshes = Array((self.arg.num_meshes,), MeshDataWrap, self.context, 0, None)
		if self.context.version == 13 and self.arg.last_count:
			self.pre_bones = ZTPreBones(self.context, 0, None)
		if self.context.version == 7 and self.arg.last_count:
			self.pre_bones = DLAPreBones(self.context, 0, None)
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
		instance.lods = Array.from_stream(stream, (instance.arg.num_lods,), LodInfo, instance.context, 0, None)
		instance.objects = Array.from_stream(stream, (instance.arg.num_objects,), Object, instance.context, 0, None)
		if instance.context.version <= 13 and (instance.arg.num_materials + instance.arg.num_objects) % 2:
			instance.objects_padding = stream.read_uint()
		instance.meshes = Array.from_stream(stream, (instance.arg.num_meshes,), MeshDataWrap, instance.context, 0, None)
		if instance.context.version == 13 and instance.arg.last_count:
			instance.pre_bones = ZTPreBones.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 7 and instance.arg.last_count:
			instance.pre_bones = DLAPreBones.from_stream(stream, instance.context, 0, None)
		if instance.context.version <= 32:
			instance.floatsy = Array.from_stream(stream, (instance.arg.render_flag,), FloatsY, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		Array.to_stream(stream, instance.materials, (instance.arg.num_materials,), MaterialName, instance.context, 0, None)
		Array.to_stream(stream, instance.lods, (instance.arg.num_lods,), LodInfo, instance.context, 0, None)
		Array.to_stream(stream, instance.objects, (instance.arg.num_objects,), Object, instance.context, 0, None)
		if instance.context.version <= 13 and (instance.arg.num_materials + instance.arg.num_objects) % 2:
			stream.write_uint(instance.objects_padding)
		Array.to_stream(stream, instance.meshes, (instance.arg.num_meshes,), MeshDataWrap, instance.context, 0, None)
		if instance.context.version == 13 and instance.arg.last_count:
			ZTPreBones.to_stream(stream, instance.pre_bones)
		if instance.context.version == 7 and instance.arg.last_count:
			DLAPreBones.to_stream(stream, instance.pre_bones)
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

	def get_info_str(self, indent=0):
		return f'Model [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* materials = {fmt_member(self.materials, indent+1)}'
		s += f'\n	* lods = {fmt_member(self.lods, indent+1)}'
		s += f'\n	* objects = {fmt_member(self.objects, indent+1)}'
		s += f'\n	* objects_padding = {fmt_member(self.objects_padding, indent+1)}'
		s += f'\n	* meshes = {fmt_member(self.meshes, indent+1)}'
		s += f'\n	* pre_bones = {fmt_member(self.pre_bones, indent+1)}'
		s += f'\n	* floatsy = {fmt_member(self.floatsy, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
