import numpy
import typing
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

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# name pointers for each material
		self.materials = Array(self.context)
		self.lods = Array(self.context)

		# lod info for each level, only present if models are present (despite the count sometimes saying otherwise!)
		self.lods = Array(self.context)

		# instantiate the meshes with materials
		self.objects = Array(self.context)

		# pad to 8 bytes alignment
		# rhino: start of model - end of objects: 124 - 4 bytes padding
		# ele: start of model - end of objects: 120 - 0 bytes padding
		self.objects_padding = 0

		# mesh data blocks for this model
		self.meshes = Array(self.context)
		self.meshes = Array(self.context)
		self.meshes = Array(self.context)

		# ?
		self.ztuac_pre_bones = ZTPreBones(self.context, None, None)

		# see if it is a flag for ztuac too, so might be totally wrong here
		self.floatsy = Array(self.context)
		self.set_defaults()

	def set_defaults(self):
		self.materials = Array(self.context)
		if self.context.version <= 13:
			self.lods = Array(self.context)
		if self.context.version >= 32 and self.arg.num_meshes:
			self.lods = Array(self.context)
		self.objects = Array(self.context)
		if self.context.version <= 13 and (self.arg.num_materials + self.arg.num_objects) % 2:
			self.objects_padding = 0
		if self.context.version >= 47:
			self.meshes = Array(self.context)
		if self.context.version == 32:
			self.meshes = Array(self.context)
		if self.context.version == 13:
			self.meshes = Array(self.context)
		if self.context.version == 13 and self.arg.last_count:
			self.ztuac_pre_bones = ZTPreBones(self.context, None, None)
		if self.context.version <= 32:
			self.floatsy = Array(self.context)

	def read(self, stream):
		self.io_start = stream.tell()
		self.materials.read(stream, MaterialName, self.arg.num_materials, None)
		if self.context.version <= 13:
			self.lods.read(stream, LodInfoZT, self.arg.num_lods, None)
		if self.context.version >= 32 and self.arg.num_meshes:
			self.lods.read(stream, LodInfo, self.arg.num_lods, None)
		self.objects.read(stream, Object, self.arg.num_objects, None)
		if self.context.version <= 13 and (self.arg.num_materials + self.arg.num_objects) % 2:
			self.objects_padding = stream.read_uint()
		if self.context.version >= 47:
			self.meshes.read(stream, NewMeshData, self.arg.num_meshes, None)
		if self.context.version == 32:
			self.meshes.read(stream, PcMeshData, self.arg.num_meshes, None)
		if self.context.version == 13:
			self.meshes.read(stream, ZtMeshData, self.arg.num_meshes, None)
		if self.context.version == 13 and self.arg.last_count:
			self.ztuac_pre_bones = stream.read_type(ZTPreBones, (self.context, None, None))
		if self.context.version <= 32:
			self.floatsy.read(stream, FloatsY, self.arg.render_flag, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.materials.write(stream, MaterialName, self.arg.num_materials, None)
		if self.context.version <= 13:
			self.lods.write(stream, LodInfoZT, self.arg.num_lods, None)
		if self.context.version >= 32 and self.arg.num_meshes:
			self.lods.write(stream, LodInfo, self.arg.num_lods, None)
		self.objects.write(stream, Object, self.arg.num_objects, None)
		if self.context.version <= 13 and (self.arg.num_materials + self.arg.num_objects) % 2:
			stream.write_uint(self.objects_padding)
		if self.context.version >= 47:
			self.meshes.write(stream, NewMeshData, self.arg.num_meshes, None)
		if self.context.version == 32:
			self.meshes.write(stream, PcMeshData, self.arg.num_meshes, None)
		if self.context.version == 13:
			self.meshes.write(stream, ZtMeshData, self.arg.num_meshes, None)
		if self.context.version == 13 and self.arg.last_count:
			stream.write_type(self.ztuac_pre_bones)
		if self.context.version <= 32:
			self.floatsy.write(stream, FloatsY, self.arg.render_flag, None)

		self.io_size = stream.tell() - self.io_start

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
