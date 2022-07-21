from source.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.cinematic.compound.EventsList
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class State(MemStruct):

	"""
	JWE2: 64 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default=False)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.a = 0
		self.b = 0
		self.c = 0
		self.d = 0
		self.abstract_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.concrete_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.debug_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.events_list = Pointer(self.context, 0, generated.formats.cinematic.compound.EventsList.EventsList)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.a = 0
		self.b = 0
		self.c = 0
		self.d = 0
		self.abstract_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.concrete_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.debug_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.events_list = Pointer(self.context, 0, generated.formats.cinematic.compound.EventsList.EventsList)

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
		instance.abstract_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.concrete_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.debug_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.a = stream.read_uint64()
		instance.b = stream.read_uint64()
		instance.c = stream.read_uint64()
		instance.events_list = Pointer.from_stream(stream, instance.context, 0, generated.formats.cinematic.compound.EventsList.EventsList)
		instance.d = stream.read_uint64()
		instance.abstract_name.arg = 0
		instance.concrete_name.arg = 0
		instance.debug_name.arg = 0
		instance.events_list.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.abstract_name)
		Pointer.to_stream(stream, instance.concrete_name)
		Pointer.to_stream(stream, instance.debug_name)
		stream.write_uint64(instance.a)
		stream.write_uint64(instance.b)
		stream.write_uint64(instance.c)
		Pointer.to_stream(stream, instance.events_list)
		stream.write_uint64(instance.d)

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
		return f'State [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* abstract_name = {fmt_member(self.abstract_name, indent+1)}'
		s += f'\n	* concrete_name = {fmt_member(self.concrete_name, indent+1)}'
		s += f'\n	* debug_name = {fmt_member(self.debug_name, indent+1)}'
		s += f'\n	* a = {fmt_member(self.a, indent+1)}'
		s += f'\n	* b = {fmt_member(self.b, indent+1)}'
		s += f'\n	* c = {fmt_member(self.c, indent+1)}'
		s += f'\n	* events_list = {fmt_member(self.events_list, indent+1)}'
		s += f'\n	* d = {fmt_member(self.d, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
