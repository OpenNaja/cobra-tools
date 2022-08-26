from generated.formats.base.basic import Ubyte
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Color(MemStruct):

	"""
	4 bytes
	"""

	__name__ = 'Color'

	_import_path = 'generated.formats.fgm.compounds.Color'

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
		self.r = 0
		self.g = 0
		self.b = 0
		self.a = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.r = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.g = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.b = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.a = Ubyte.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Ubyte.to_stream(stream, instance.r)
		Ubyte.to_stream(stream, instance.g)
		Ubyte.to_stream(stream, instance.b)
		Ubyte.to_stream(stream, instance.a)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'r', Ubyte, (0, None), (False, None)
		yield 'g', Ubyte, (0, None), (False, None)
		yield 'b', Ubyte, (0, None), (False, None)
		yield 'a', Ubyte, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Color [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* r = {self.fmt_member(self.r, indent+1)}'
		s += f'\n	* g = {self.fmt_member(self.g, indent+1)}'
		s += f'\n	* b = {self.fmt_member(self.b, indent+1)}'
		s += f'\n	* a = {self.fmt_member(self.a, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
