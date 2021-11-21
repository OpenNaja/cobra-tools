from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.FloatsY import FloatsY
from generated.formats.ms2.compound.LodInfo import LodInfo
from generated.formats.ms2.compound.LodInfoZT import LodInfoZT
from generated.formats.ms2.compound.MaterialName import MaterialName
from generated.formats.ms2.compound.MeshLink import MeshLink
from generated.formats.ms2.compound.PcModelData import PcModelData
from generated.formats.ms2.compound.SmartPadding import SmartPadding
from generated.formats.ms2.compound.ZTPreBones import ZTPreBones
from generated.formats.ms2.compound.ZtModelData import ZtModelData


class PcModel:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# uses uint here, two uints elsewhere
		self.materials = Array((self.arg.num_materials,), MaterialName, self.context, 0, None)
		self.lods = Array((self.arg.num_lods,), LodInfoZT, self.context, 0, None)
		self.lods = Array((self.arg.num_lods,), LodInfo, self.context, 0, None)
		self.objects = Array((self.arg.num_objects,), MeshLink, self.context, 0, None)

		# pad to 8 bytes alignment
		self.padding = 0
		self.models = Array((self.arg.num_models,), PcModelData, self.context, 0, None)
		self.models = Array((self.arg.num_models,), ZtModelData, self.context, 0, None)
		self.ztuac_pre_bones = ZTPreBones(self.context, 0, None)

		# see if it is a flag for ztuac too, so might be totally wrong here
		self.floatsy = Array((self.arg.render_flag,), FloatsY, self.context, 0, None)

		# sometimes 00 byte
		self.weird_padding = SmartPadding(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.materials = Array((self.arg.num_materials,), MaterialName, self.context, 0, None)
		if self.context.version == 17:
			self.lods = Array((self.arg.num_lods,), LodInfoZT, self.context, 0, None)
		if self.context.version == 18:
			self.lods = Array((self.arg.num_lods,), LodInfo, self.context, 0, None)
		self.objects = Array((self.arg.num_objects,), MeshLink, self.context, 0, None)
		if self.context.version == 17 and (self.arg.num_materials + self.arg.num_objects) % 2:
			self.padding = 0
		if self.context.version == 18:
			self.models = Array((self.arg.num_models,), PcModelData, self.context, 0, None)
		if self.context.version == 17:
			self.models = Array((self.arg.num_models,), ZtModelData, self.context, 0, None)
		if self.context.version == 17 and self.arg.last_count:
			self.ztuac_pre_bones = ZTPreBones(self.context, 0, None)
		self.floatsy = Array((self.arg.render_flag,), FloatsY, self.context, 0, None)
		self.weird_padding = SmartPadding(self.context, 0, None)

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
		if instance.context.version == 17:
			instance.lods = Array.from_stream(stream, (instance.arg.num_lods,), LodInfoZT, instance.context, 0, None)
		if instance.context.version == 18:
			instance.lods = Array.from_stream(stream, (instance.arg.num_lods,), LodInfo, instance.context, 0, None)
		instance.objects = Array.from_stream(stream, (instance.arg.num_objects,), MeshLink, instance.context, 0, None)
		if instance.context.version == 17 and (instance.arg.num_materials + instance.arg.num_objects) % 2:
			instance.padding = stream.read_uint()
		if instance.context.version == 18:
			instance.models = Array.from_stream(stream, (instance.arg.num_models,), PcModelData, instance.context, 0, None)
		if instance.context.version == 17:
			instance.models = Array.from_stream(stream, (instance.arg.num_models,), ZtModelData, instance.context, 0, None)
		if instance.context.version == 17 and instance.arg.last_count:
			instance.ztuac_pre_bones = ZTPreBones.from_stream(stream, instance.context, 0, None)
		instance.floatsy = Array.from_stream(stream, (instance.arg.render_flag,), FloatsY, instance.context, 0, None)
		instance.weird_padding = SmartPadding.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		Array.to_stream(stream, instance.materials, (instance.arg.num_materials,),MaterialName, instance.context, 0, None)
		if instance.context.version == 17:
			Array.to_stream(stream, instance.lods, (instance.arg.num_lods,),LodInfoZT, instance.context, 0, None)
		if instance.context.version == 18:
			Array.to_stream(stream, instance.lods, (instance.arg.num_lods,),LodInfo, instance.context, 0, None)
		Array.to_stream(stream, instance.objects, (instance.arg.num_objects,),MeshLink, instance.context, 0, None)
		if instance.context.version == 17 and (instance.arg.num_materials + instance.arg.num_objects) % 2:
			stream.write_uint(instance.padding)
		if instance.context.version == 18:
			Array.to_stream(stream, instance.models, (instance.arg.num_models,),PcModelData, instance.context, 0, None)
		if instance.context.version == 17:
			Array.to_stream(stream, instance.models, (instance.arg.num_models,),ZtModelData, instance.context, 0, None)
		if instance.context.version == 17 and instance.arg.last_count:
			ZTPreBones.to_stream(stream, instance.ztuac_pre_bones)
		Array.to_stream(stream, instance.floatsy, (instance.arg.render_flag,),FloatsY, instance.context, 0, None)
		SmartPadding.to_stream(stream, instance.weird_padding)

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
		return f'PcModel [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* materials = {self.materials.__repr__()}'
		s += f'\n	* lods = {self.lods.__repr__()}'
		s += f'\n	* objects = {self.objects.__repr__()}'
		s += f'\n	* padding = {self.padding.__repr__()}'
		s += f'\n	* models = {self.models.__repr__()}'
		s += f'\n	* ztuac_pre_bones = {self.ztuac_pre_bones.__repr__()}'
		s += f'\n	* floatsy = {self.floatsy.__repr__()}'
		s += f'\n	* weird_padding = {self.weird_padding.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
