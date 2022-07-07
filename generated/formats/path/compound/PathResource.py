from source.formats.base.basic import fmt_member
import generated.formats.base.basic
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class PathResource(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.path_type = 0
		self.path_sub_type = 0
		self.unk_byte_1 = 0
		self.unk_byte_2 = 0
		self.padding = 0
		self.pathmaterial = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.pathextrusion_kerb = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.pathextrusion_railing = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.pathextrusion_ground = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.pathsupport = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.path_type = 0
		self.path_sub_type = 0
		self.unk_byte_1 = 0
		self.unk_byte_2 = 0
		self.padding = 0
		self.pathmaterial = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.pathextrusion_kerb = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.pathextrusion_railing = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.pathextrusion_ground = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.pathsupport = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.pathmaterial = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.pathextrusion_kerb = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.pathextrusion_railing = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.pathextrusion_ground = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.pathsupport = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.path_type = stream.read_byte()
		instance.path_sub_type = stream.read_byte()
		instance.unk_byte_1 = stream.read_byte()
		instance.unk_byte_2 = stream.read_byte()
		instance.padding = stream.read_uint()
		instance.pathmaterial.arg = 0
		instance.pathextrusion_kerb.arg = 0
		instance.pathextrusion_railing.arg = 0
		instance.pathextrusion_ground.arg = 0
		instance.pathsupport.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.pathmaterial)
		Pointer.to_stream(stream, instance.pathextrusion_kerb)
		Pointer.to_stream(stream, instance.pathextrusion_railing)
		Pointer.to_stream(stream, instance.pathextrusion_ground)
		Pointer.to_stream(stream, instance.pathsupport)
		stream.write_byte(instance.path_type)
		stream.write_byte(instance.path_sub_type)
		stream.write_byte(instance.unk_byte_1)
		stream.write_byte(instance.unk_byte_2)
		stream.write_uint(instance.padding)

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
		return f'PathResource [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* pathmaterial = {fmt_member(self.pathmaterial, indent+1)}'
		s += f'\n	* pathextrusion_kerb = {fmt_member(self.pathextrusion_kerb, indent+1)}'
		s += f'\n	* pathextrusion_railing = {fmt_member(self.pathextrusion_railing, indent+1)}'
		s += f'\n	* pathextrusion_ground = {fmt_member(self.pathextrusion_ground, indent+1)}'
		s += f'\n	* pathsupport = {fmt_member(self.pathsupport, indent+1)}'
		s += f'\n	* path_type = {fmt_member(self.path_type, indent+1)}'
		s += f'\n	* path_sub_type = {fmt_member(self.path_sub_type, indent+1)}'
		s += f'\n	* unk_byte_1 = {fmt_member(self.unk_byte_1, indent+1)}'
		s += f'\n	* unk_byte_2 = {fmt_member(self.unk_byte_2, indent+1)}'
		s += f'\n	* padding = {fmt_member(self.padding, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
