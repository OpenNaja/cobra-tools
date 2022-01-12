import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.LodInfo import LodInfo
from generated.formats.ms2.compound.MaterialName import MaterialName
from generated.formats.ms2.compound.MeshData import MeshData
from generated.formats.ms2.compound.Object import Object


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

		# lod info for each level, only present if models are present (despite the count sometimes saying otherwise!)
		self.lods = Array(self.context)

		# instantiate the meshes with materials
		self.objects = Array(self.context)

		# mesh data blocks for this model
		self.meshes = Array(self.context)
		self.set_defaults()

	def set_defaults(self):
		self.materials = Array(self.context)
		if self.arg.num_meshes:
			self.lods = Array(self.context)
		self.objects = Array(self.context)
		self.meshes = Array(self.context)

	def read(self, stream):
		self.io_start = stream.tell()
		self.materials.read(stream, MaterialName, self.arg.num_materials, None)
		if self.arg.num_meshes:
			self.lods.read(stream, LodInfo, self.arg.num_lods, None)
		self.objects.read(stream, Object, self.arg.num_objects, None)
		self.meshes.read(stream, MeshData, self.arg.num_meshes, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.materials.write(stream, MaterialName, self.arg.num_materials, None)
		if self.arg.num_meshes:
			self.lods.write(stream, LodInfo, self.arg.num_lods, None)
		self.objects.write(stream, Object, self.arg.num_objects, None)
		self.meshes.write(stream, MeshData, self.arg.num_meshes, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Model [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* materials = {self.materials.__repr__()}'
		s += f'\n	* lods = {self.lods.__repr__()}'
		s += f'\n	* objects = {self.objects.__repr__()}'
		s += f'\n	* meshes = {self.meshes.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
