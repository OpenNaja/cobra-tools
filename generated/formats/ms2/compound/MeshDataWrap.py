from source.formats.base.basic import fmt_member
from generated.formats.ms2.compound.BioMeshData import BioMeshData
from generated.formats.ms2.compound.NewMeshData import NewMeshData
from generated.formats.ms2.compound.PcMeshData import PcMeshData
from generated.formats.ms2.compound.ZtMeshData import ZtMeshData
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class MeshDataWrap(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default=False)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.mesh = BioMeshData(self.context, 0, None)
		self.mesh = NewMeshData(self.context, 0, None)
		self.mesh = PcMeshData(self.context, 0, None)
		self.mesh = ZtMeshData(self.context, 0, None)
		self.mesh = ZtMeshData(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		if self.context.version >= 47 and (self.context.version == 51) and self.context.biosyn:
			self.mesh = BioMeshData(self.context, 0, None)
		if self.context.version >= 47 and not ((self.context.version == 51) and self.context.biosyn):
			self.mesh = NewMeshData(self.context, 0, None)
		if self.context.version == 32:
			self.mesh = PcMeshData(self.context, 0, None)
		if self.context.version == 13:
			self.mesh = ZtMeshData(self.context, 0, None)
		if self.context.version == 7:
			self.mesh = ZtMeshData(self.context, 0, None)

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
		if instance.context.version >= 47 and (instance.context.version == 51) and instance.context.biosyn:
			instance.mesh = BioMeshData.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			instance.mesh = NewMeshData.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 32:
			instance.mesh = PcMeshData.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 13:
			instance.mesh = ZtMeshData.from_stream(stream, instance.context, 0, None)
		if instance.context.version == 7:
			instance.mesh = ZtMeshData.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.context.version >= 47 and (instance.context.version == 51) and instance.context.biosyn:
			BioMeshData.to_stream(stream, instance.mesh)
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			NewMeshData.to_stream(stream, instance.mesh)
		if instance.context.version == 32:
			PcMeshData.to_stream(stream, instance.mesh)
		if instance.context.version == 13:
			ZtMeshData.to_stream(stream, instance.mesh)
		if instance.context.version == 7:
			ZtMeshData.to_stream(stream, instance.mesh)

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
		return f'MeshDataWrap [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* mesh = {fmt_member(self.mesh, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
