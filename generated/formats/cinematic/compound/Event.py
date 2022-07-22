from source.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.cinematic.compound.EventAttributes
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class Event(MemStruct):

	"""
	32 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.start_time = 0.0
		self.b = 0.0
		self.duration = 0.0
		self.d = 0.0
		self.module_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.attributes = Pointer(self.context, 0, generated.formats.cinematic.compound.EventAttributes.EventAttributes)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.start_time = 0.0
		self.b = 0.0
		self.duration = 0.0
		self.d = 0.0
		self.module_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.attributes = Pointer(self.context, 0, generated.formats.cinematic.compound.EventAttributes.EventAttributes)

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
		instance.start_time = stream.read_float()
		instance.b = stream.read_float()
		instance.module_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.attributes = Pointer.from_stream(stream, instance.context, 0, generated.formats.cinematic.compound.EventAttributes.EventAttributes)
		instance.duration = stream.read_float()
		instance.d = stream.read_float()
		instance.module_name.arg = 0
		instance.attributes.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_float(instance.start_time)
		stream.write_float(instance.b)
		Pointer.to_stream(stream, instance.module_name)
		Pointer.to_stream(stream, instance.attributes)
		stream.write_float(instance.duration)
		stream.write_float(instance.d)

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
		return f'Event [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* start_time = {fmt_member(self.start_time, indent+1)}'
		s += f'\n	* b = {fmt_member(self.b, indent+1)}'
		s += f'\n	* module_name = {fmt_member(self.module_name, indent+1)}'
		s += f'\n	* attributes = {fmt_member(self.attributes, indent+1)}'
		s += f'\n	* duration = {fmt_member(self.duration, indent+1)}'
		s += f'\n	* d = {fmt_member(self.d, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
