from source.formats.base.basic import fmt_member
from generated.formats.base.basic import Ubyte
from generated.struct import StructBase


class Triplet(StructBase):

	"""
	3 bytes - constant per mime (and probably version)
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# ?
		self.a = 0

		# ?
		self.b = 0

		# ?
		self.c = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.a = 0
		self.b = 0
		self.c = 0

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
		instance.a = stream.read_ubyte()
		instance.b = stream.read_ubyte()
		instance.c = stream.read_ubyte()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_ubyte(instance.a)
		stream.write_ubyte(instance.b)
		stream.write_ubyte(instance.c)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('a', Ubyte, (0, None))
		yield ('b', Ubyte, (0, None))
		yield ('c', Ubyte, (0, None))

	def get_info_str(self, indent=0):
		return f'Triplet [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* a = {fmt_member(self.a, indent+1)}'
		s += f'\n	* b = {fmt_member(self.b, indent+1)}'
		s += f'\n	* c = {fmt_member(self.c, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s

	def __eq__(self, other):
		if isinstance(other, Triplet):
			return self.a == other.a and self.b == other.b and self.c == other.c

