from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class SplRoot(MemStruct):

	"""
	JWE2: 16 bytes
	very weird, related to count
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.sixteen = 0
		self.one = 0
		self.length = 0
		self.spline_data = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
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
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('spline_data', Pointer, (instance.count, None))
		yield ('count', Ushort, (0, None))
		yield ('sixteen', Ubyte, (0, None))
		yield ('one', Ubyte, (0, None))
		yield ('length', Float, (0, None))

	def get_info_str(self, indent=0):
		return f'SplRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* spline_data = {self.fmt_member(self.spline_data, indent+1)}'
		s += f'\n	* count = {self.fmt_member(self.count, indent+1)}'
		s += f'\n	* sixteen = {self.fmt_member(self.sixteen, indent+1)}'
		s += f'\n	* one = {self.fmt_member(self.one, indent+1)}'
		s += f'\n	* length = {self.fmt_member(self.length, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
