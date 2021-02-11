import typing
from generated.array import Array
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

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# uses uint here, two uints elsewhere
		self.materials = Array()
		self.lods = Array()
		self.lods = Array()
		self.mesh_links = Array()

		# may be padding instead
		self.unk = 0
		self.models = Array()
		self.models = Array()
		self.ztuac_pre_bones = ZTPreBones()
		self.floatsy = Array()

		# sometimes 00 byte
		self.weird_padding = SmartPadding()

	def read(self, stream):

		self.io_start = stream.tell()
		self.materials.read(stream, MaterialName, self.arg.mat_count, None)
		if stream.version == 17:
			self.lods.read(stream, LodInfoZT, self.arg.lod_count, None)
		if stream.version == 18:
			self.lods.read(stream, LodInfo, self.arg.lod_count, None)
		self.mesh_links.read(stream, MeshLink, self.arg.mesh_link_count, None)
		if self.arg.another_count:
			self.unk = stream.read_uint()
		if stream.version == 18:
			self.models.read(stream, PcModelData, self.arg.model_count, None)
		if stream.version == 17:
			self.models.read(stream, ZtModelData, self.arg.model_count, None)
			self.ztuac_pre_bones = stream.read_type(ZTPreBones)
		self.floatsy.read(stream, FloatsY, self.arg.another_count, None)
		self.weird_padding = stream.read_type(SmartPadding)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		self.materials.write(stream, MaterialName, self.arg.mat_count, None)
		if stream.version == 17:
			self.lods.write(stream, LodInfoZT, self.arg.lod_count, None)
		if stream.version == 18:
			self.lods.write(stream, LodInfo, self.arg.lod_count, None)
		self.mesh_links.write(stream, MeshLink, self.arg.mesh_link_count, None)
		if self.arg.another_count:
			stream.write_uint(self.unk)
		if stream.version == 18:
			self.models.write(stream, PcModelData, self.arg.model_count, None)
		if stream.version == 17:
			self.models.write(stream, ZtModelData, self.arg.model_count, None)
			stream.write_type(self.ztuac_pre_bones)
		self.floatsy.write(stream, FloatsY, self.arg.another_count, None)
		stream.write_type(self.weird_padding)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'PcModel [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* materials = {self.materials.__repr__()}'
		s += f'\n	* lods = {self.lods.__repr__()}'
		s += f'\n	* mesh_links = {self.mesh_links.__repr__()}'
		s += f'\n	* unk = {self.unk.__repr__()}'
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
