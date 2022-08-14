from generated.formats.base.basic import Float
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.spl.compounds.ByteVector3 import ByteVector3
from generated.formats.spl.compounds.ShortVector3 import ShortVector3


class Key(MemStruct):

	"""
	JWE2: 16 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.pos = ShortVector3(self.context, 0, None)
		self.handle_a = ByteVector3(self.context, 0, None)
		self.handle_b = ByteVector3(self.context, 0, None)
		self.handle_size = 0.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.pos = ShortVector3(self.context, 0, None)
		self.handle_a = ByteVector3(self.context, 0, None)
		self.handle_b = ByteVector3(self.context, 0, None)
		self.handle_size = 0.0

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
		instance.pos = ShortVector3.from_stream(stream, instance.context, 0, None)
		instance.handle_a = ByteVector3.from_stream(stream, instance.context, 0, None)
		instance.handle_b = ByteVector3.from_stream(stream, instance.context, 0, None)
		instance.handle_size = stream.read_float()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		ShortVector3.to_stream(stream, instance.pos)
		ByteVector3.to_stream(stream, instance.handle_a)
		ByteVector3.to_stream(stream, instance.handle_b)
		stream.write_float(instance.handle_size)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'pos', ShortVector3, (0, None)
		yield 'handle_a', ByteVector3, (0, None)
		yield 'handle_b', ByteVector3, (0, None)
		yield 'handle_size', Float, (0, None)

	def get_info_str(self, indent=0):
		return f'Key [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* pos = {self.fmt_member(self.pos, indent+1)}'
		s += f'\n	* handle_a = {self.fmt_member(self.handle_a, indent+1)}'
		s += f'\n	* handle_b = {self.fmt_member(self.handle_b, indent+1)}'
		s += f'\n	* handle_size = {self.fmt_member(self.handle_size, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
