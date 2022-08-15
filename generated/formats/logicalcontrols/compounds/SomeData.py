from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class SomeData(MemStruct):

	"""
	16 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.key = 0
		self.extra = 0
		self.a = 0.0
		self.b = 0.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.key = 0
		self.extra = 0
		self.a = 0.0
		self.b = 0.0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.key = Uint.from_stream(stream, instance.context, 0, None)
		instance.extra = Uint.from_stream(stream, instance.context, 0, None)
		instance.a = Float.from_stream(stream, instance.context, 0, None)
		instance.b = Float.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.key)
		stream.write_uint(instance.extra)
		stream.write_float(instance.a)
		stream.write_float(instance.b)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'key', Uint, (0, None)
		yield 'extra', Uint, (0, None)
		yield 'a', Float, (0, None)
		yield 'b', Float, (0, None)

	def get_info_str(self, indent=0):
		return f'SomeData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* key = {self.fmt_member(self.key, indent+1)}'
		s += f'\n	* extra = {self.fmt_member(self.extra, indent+1)}'
		s += f'\n	* a = {self.fmt_member(self.a, indent+1)}'
		s += f'\n	* b = {self.fmt_member(self.b, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
