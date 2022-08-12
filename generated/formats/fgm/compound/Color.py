from generated.formats.base.basic import fmt_member
from generated.formats.base.basic import Ubyte
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class Color(MemStruct):

	"""
	4 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.r = 0
		self.g = 0
		self.b = 0
		self.a = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.r = 0
		self.g = 0
		self.b = 0
		self.a = 0

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
		instance.r = stream.read_ubyte()
		instance.g = stream.read_ubyte()
		instance.b = stream.read_ubyte()
		instance.a = stream.read_ubyte()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_ubyte(instance.r)
		stream.write_ubyte(instance.g)
		stream.write_ubyte(instance.b)
		stream.write_ubyte(instance.a)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('r', Ubyte, (0, None))
		yield ('g', Ubyte, (0, None))
		yield ('b', Ubyte, (0, None))
		yield ('a', Ubyte, (0, None))

	def get_info_str(self, indent=0):
		return f'Color [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* r = {fmt_member(self.r, indent+1)}'
		s += f'\n	* g = {fmt_member(self.g, indent+1)}'
		s += f'\n	* b = {fmt_member(self.b, indent+1)}'
		s += f'\n	* a = {fmt_member(self.a, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
