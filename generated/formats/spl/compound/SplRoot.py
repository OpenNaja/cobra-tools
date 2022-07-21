from source.formats.base.basic import fmt_member
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class SplRoot(MemStruct):

	"""
	JWE2: 16 bytes
	very weird, related to count
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default=False)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.count = 0
		self.sixteen = 0
		self.one = 0
		self.length = 0.0
		self.spline_data = Pointer(self.context, self.count, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count = 0
		self.sixteen = 0
		self.one = 0
		self.length = 0.0
		self.spline_data = Pointer(self.context, self.count, None)

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
		instance.spline_data = Pointer.from_stream(stream, instance.context, instance.count, None)
		instance.count = stream.read_ushort()
		instance.sixteen = stream.read_ubyte()
		instance.one = stream.read_ubyte()
		instance.length = stream.read_float()
		instance.spline_data.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.spline_data)
		stream.write_ushort(instance.count)
		stream.write_ubyte(instance.sixteen)
		stream.write_ubyte(instance.one)
		stream.write_float(instance.length)

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
		return f'SplRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* spline_data = {fmt_member(self.spline_data, indent+1)}'
		s += f'\n	* count = {fmt_member(self.count, indent+1)}'
		s += f'\n	* sixteen = {fmt_member(self.sixteen, indent+1)}'
		s += f'\n	* one = {fmt_member(self.one, indent+1)}'
		s += f'\n	* length = {fmt_member(self.length, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
