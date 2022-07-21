from source.formats.base.basic import fmt_member
import generated.formats.base.basic
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class FontInfo(MemStruct):

	"""
	24 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default=False)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.flag_or_count = 0
		self.style_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.font_file = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.flag_or_count = 0
		self.style_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.font_file = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.style_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.font_file = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.flag_or_count = stream.read_uint64()
		instance.style_name.arg = 0
		instance.font_file.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.style_name)
		Pointer.to_stream(stream, instance.font_file)
		stream.write_uint64(instance.flag_or_count)

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
		return f'FontInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* style_name = {fmt_member(self.style_name, indent+1)}'
		s += f'\n	* font_file = {fmt_member(self.font_file, indent+1)}'
		s += f'\n	* flag_or_count = {fmt_member(self.flag_or_count, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
