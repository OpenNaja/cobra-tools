from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte


class Triplet(BaseStruct):

	"""
	3 bytes - constant per mime (and probably version)
	"""

	__name__ = 'Triplet'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# ?
		self.a = 0

		# ?
		self.b = 0

		# ?
		self.c = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.a = 0
		self.b = 0
		self.c = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.a = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.b = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.c = Ubyte.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Ubyte.to_stream(stream, instance.a)
		Ubyte.to_stream(stream, instance.b)
		Ubyte.to_stream(stream, instance.c)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'a', Ubyte, (0, None), (False, None)
		yield 'b', Ubyte, (0, None), (False, None)
		yield 'c', Ubyte, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Triplet [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* a = {self.fmt_member(self.a, indent+1)}'
		s += f'\n	* b = {self.fmt_member(self.b, indent+1)}'
		s += f'\n	* c = {self.fmt_member(self.c, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s

	def __eq__(self, other):
		if isinstance(other, Triplet):
			return self.a == other.a and self.b == other.b and self.c == other.c

